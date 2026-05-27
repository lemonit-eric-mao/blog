---
title: "Collabora CODE 服务部署"
date: "2026-05-27"
categories: 
  - "linux"
---





# Collabora/CODE 服务部署



## 部署

``` bash
# 1. 确保创建并进入单独的服务目录
mkdir -p ./collabora-service && cd ./collabora-service

# 2. 【核心安全保障】检查并创建名为 dev-infra-network 的外部共享桥接网络
# 这样可以让它不仅能跟之前的 RustFS 通信，以后你自研的后端容器加进来也能无缝互通
docker network inspect dev-infra-network >/dev/null 2>&1 || docker network create --driver bridge dev-infra-network

# 3. 写入独立的 docker-compose.yaml 文件（已集成容器健康检查机制）
cat << 'EOF' > docker-compose.yaml
services:
  collabora:
    image: collabora/code:25.04.9.4.1
    container_name: dev-collabora
    ports:
      - "9980:9980"           # 宿主机映射端口：供你的公文系统前端页面通过 iframe 嵌入
    environment:
      # ====== 核心域/IP安全白名单（极其重要） ======
      # 作用：限制哪些来源的网页可以调用本 Office 引擎。
      # 本地或测试环境使用通配符 'http://.*,https://.*' 允许任意前端系统调用。
      # 生产环境为了防盗刷，必须改成你自研公文系统的真实域名（例如：'http://oa.yourcompany.com'）
      - aliasgroup1=http://.*,https://.*

      # ====== 彻底关闭内置 SSL 证书（开发福音） ======
      # DONT_GEN_SSL_CERTS: 告诉容器不要在启动时去自己生成那些烦人的、会过期的自签名证书
      - DONT_GEN_SSL_CERTS=true
      # extra_params: 通过底层参数彻底关掉内置的 HTTPS 强制重定向和 SSL 终止机制
      # 这样你本地接口联调时全走纯 HTTP 模式，用 F12 或抓包工具看 WOPI 协议的数据流一目了然
      - extra_params=--o:ssl.enable=false --o:ssl.termination=false
    
    # ====== 🐋 容器健康检查（Healthcheck） ======
    healthcheck:
      # 借用容器内部的 curl 去请求 9980 端口的发现服务接口。-f 表示遇到 HTTP 错误直接返回非0状态
      test: ["CMD", "curl", "-f", "http://localhost:9980/hosting/discovery"]
      interval: 10s           # 每隔 10 秒进行一次健康检查
      timeout: 5s             # 单次探测如果超过 5 秒没有响应，则视为单次失败
      retries: 3              # 连续失败 3 次后，该容器会被 Docker 判定为 "unhealthy"
      start_period: 10s       # 容器启动后的前 10 秒为缓冲期，此时发生的探测失败不计入总数（给服务留出初始化时间）

    networks:
      - dev-infra-network     # 挂载到外部共享桥接网络中
    restart: unless-stopped

# 声明并加入已存在的外部共享网络
networks:
  dev-infra-network:
    external: true            # 标记为外部网络，防止本 compose 销毁时误连带删除网络
    name: dev-infra-network
EOF

# 4. 直接在后台一键拉取镜像并启动（或覆盖更新）
docker compose up -d
```

查看

``` bash
[cloud@New-test1 (16:02:41) /mnt/data/siyu.mao/collabora-service]
└─$ docker-compose ps
NAME            IMAGE                        COMMAND                   SERVICE     CREATED         STATUS                            PORTS
dev-collabora   collabora/code:25.04.9.4.1   "/start-collabora-on…"   collabora   6 seconds ago   Up 5 seconds (health: starting)   0.0.0.0:9980->9980/tcp, :::9980->9980/tcp

```







## 测试



#### 运行 FastAPI “传声筒”脚本

请确保你的测试环境安装了 FastAPI 和 S3 客户端库：

```bash
pip install fastapi uvicorn boto3
```

然后，在你的开发机或服务器上，创建并运行以下 **`wopi_fastapi.py`** 脚本：

```python
import io
import mimetypes
import boto3
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic_settings import BaseSettings, SettingsConfigDict

# ====== 1. 统一配置管理中心 ======
class Settings(BaseSettings):
    # --- RustFS (S3) 配置 ---
    # FastAPI 与 RustFS 在同一台机器，走内网 IP + 内部端口 9000，无需绕外网
    rustfs_endpoint: str = "http://10.10.0.2:9000"
    rustfs_access_key: str = "admin_access_key_xyz789"
    rustfs_secret_key: str = "admin_secret_key_pro456file"
    rustfs_bucket_name: str = "official-documents"

    # --- 核心网络：同机内网交互配置 ---
    # 供远程浏览器访问的 CODE 外网地址（浏览器从外网打开 Collabora 编辑器）
    collabora_public_host: str = "http://221.180.141.96:9980"

    # 供云端 CODE 容器回调 WOPI 接口的内网地址
    # CODE 与 FastAPI 在同一台机器，走内网 IP + 内部端口 8001
    fastapi_internal_host: str = "http://10.10.0.2:8001"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# ====== 2. 初始化服务与客户端 ======
app = FastAPI(title="公文系统 WOPI 同机混合网络联调控制台")

# 允许跨域：浏览器从外网访问 FastAPI，同时 Collabora 也需要跨域请求 WOPI 接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(
    's3',
    endpoint_url=settings.rustfs_endpoint,
    aws_access_key_id=settings.rustfs_access_key,
    aws_secret_access_key=settings.rustfs_secret_key
)

# ====== 3. 前端测试页面：智能混合链接拼接 ======
@app.get("/", response_class=HTMLResponse)
async def index():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>自研公文系统 - 云端同机联调控制台</title>
        <style>
            body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; font-family: sans-serif; }}
            .control-panel {{ padding: 15px; background: #f5f5f5; border-bottom: 1px solid #ddd; display: flex; gap: 10px; align-items: center; }}
            input {{ padding: 8px; width: 450px; border: 1px solid #ccc; border-radius: 4px; }}
            button {{ padding: 8px 15px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }}
            button:hover {{ background: #218838; }}
            .iframe-container {{ width: 100%; height: calc(100vh - 70px); background: #eee; }}
            iframe {{ width: 100%; height: 100%; border: none; }}
        </style>
    </head>
    <body>

        <div class="control-panel">
            <label><b>请输入 RustFS 中的文件名：</b></label>
            <input type="text" id="fileIdInput" value="华能吉林发电有限公司品牌建设2026年重点任务.xls" placeholder="请输入文件名，带后缀">
            <button onclick="loadDocument()">🚀 挂载并预览公文</button>
        </div>

        <div class="iframe-container" id="container">
            <div style="padding: 40px; text-align: center; color: #666;">
                服务已就绪。点击上方按钮，浏览器将通过外网加载 CODE 引擎，CODE 将通过内网（10.10.0.2）读取本服务。
            </div>
        </div>

        <script>
            function loadDocument() {{
                var fileId = document.getElementById('fileIdInput').value.trim();
                if (!fileId) {{
                    alert('请输入文件名！');
                    return;
                }}
                
                // 📢 这里的精妙之处：
                // WOPISrc 拼的是内网地址，因为是给云端同机容器看的。
                // finalUrl 拼的是外网地址，因为是给你本地浏览器看的。
                var wopiSrc = "{settings.fastapi_internal_host}" + "/wopi/files/" + encodeURIComponent(fileId);
                var finalUrl = "{settings.collabora_public_host}" + "/browser/dist/cool.html?WOPISrc=" + wopiSrc + "&access_token=MOCK_TOKEN&lang=zh-CN";
                
                var container = document.getElementById('container');
                container.innerHTML = '<iframe src="' + finalUrl + '" allowfullscreen></iframe>';
            }}
        </script>
    </body>
    </html>
    """
    return html_content

# ====== 4. WOPI 标准接口：检查文件信息 ======
@app.get("/wopi/files/{file_id}")
async def check_file_info(file_id: str):
    try:
        response = s3_client.head_object(Bucket=settings.rustfs_bucket_name, Key=file_id)
        file_size = response.get('ContentLength', 0)
    except Exception:
        raise HTTPException(status_code=404, detail=f"在 RustFS 的 [{settings.rustfs_bucket_name}] 桶中未找到文件: {file_id}")

    return {
        "BaseFileName": file_id.split('/')[-1],
        "Size": file_size,
        "OwnerId": "admin",
        "UserCanWrite": True, 
        "PostMessageOrigin": "*"
    }

# ====== 5. WOPI 标准接口：流式转发文件内容（读取） ======
@app.get("/wopi/files/{file_id}/contents")
async def get_file_contents(file_id: str):
    try:
        s3_object = s3_client.get_object(Bucket=settings.rustfs_bucket_name, Key=file_id)
        file_data = s3_object['Body'].read()
        
        content_type, _ = mimetypes.guess_type(file_id)
        if not content_type:
            if file_id.endswith('.xls'):
                content_type = "application/vnd.ms-excel"
            else:
                content_type = "application/octet-stream"
        
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ====== 6. WOPI 标准接口：保存文件内容（PutFile） ======
# Collabora 编辑完成后，会通过此接口将文件回写到 RustFS
@app.post("/wopi/files/{file_id}/contents")
async def put_file_contents(file_id: str, request: Request):
    try:
        file_data = await request.body()
        if not file_data:
            raise HTTPException(status_code=400, detail="请求体为空，未收到文件内容")
        
        content_type, _ = mimetypes.guess_type(file_id)
        if not content_type:
            content_type = "application/octet-stream"
        
        s3_client.put_object(
            Bucket=settings.rustfs_bucket_name,
            Key=file_id,
            Body=file_data,
            ContentType=content_type
        )
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # 监听 0.0.0.0 确保无论你从外网访问，还是 CODE 从内网 10.10.0.2 访问，都能接得住
    uvicorn.run(app, host="0.0.0.0", port=8001)
```



运行脚本：

```bash
uv add fastapi pydantic-settings boto3 uvicorn

uv run wopi_fastapi.py

```



现在，请打开浏览器，**直接访问 FastAPI 的主页**：

```bash
http://<你的FastAPI服务器IP>:8001/
```



此时发生的数据链路：

1. 浏览器请求 FastAPI 的 `/` 根路由，FastAPI 响应并渲染出包含了配置好 `WOPISrc` 的 `<iframe>`。
2. 浏览器解析 `<iframe>`，开始向 **Collabora (9980端口)** 请求加载编辑器壳子。
3. Collabora 收到请求后，立刻顺着 `WOPISrc` 链接，**反向调用** FastAPI 的 `/wopi/files/test.docx/contents` 接口。
4. 你的 FastAPI 收到回调，秒速去 **RustFS (9000端口)** 捞出 `test.docx` 的二进制流，原路吐回给 Collabora。
5. Collabora 拿到流，在 `<iframe>` 盒子里把你的 Word 文档完美画了出来。

你可以试着在网页的 Word 里随便打个字、改个颜色，体验一下纯自研系统里集成高端在线 Office 的核心技术魅力！



