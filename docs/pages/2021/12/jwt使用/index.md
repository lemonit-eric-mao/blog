---
title: "JWT使用"
date: "2021-12-30"
categories: 
  - "java"
  - "jwt"
  - "python"
---

### [前置资料-了解JWT](http://www.dev-share.top/2023/09/01/%e4%ba%86%e8%a7%a3jwt/ "前置资料-了解JWT")

## Python 代码示例

### 生成与校验的用法

```python
import jwt
from datetime import datetime, timedelta


# 生成JWT令牌
def generate_jwt_token(user_id):
    # 设置有效期为1小时
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    # 构建Payload，可以根据需要自定义
    payload = {
        "user_id": user_id,
        "exp": expiration_time
    }
    # 使用密钥对Payload进行签名
    jwt_token = jwt.encode(payload, "your_secret_key", algorithm="HS256")
    return jwt_token


# 解析JWT令牌
def parse_jwt_token(jwt_token):
    try:
        # 使用密钥解析JWT令牌
        payload = jwt.decode(jwt_token, "your_secret_key", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # 处理过期的JWT令牌
        return None
    except jwt.InvalidTokenError:
        # 处理无效的JWT令牌
        return None


if __name__ == "__main__":
    # 示例用法
    user_id = "a1b2c3d4"
    jwt_token = generate_jwt_token(user_id)
    print("Generated JWT Token:", jwt_token)

    decoded_payload = parse_jwt_token(jwt_token)
    if decoded_payload:
        print("Decoded Payload:", decoded_payload)
    else:
        print("Invalid or expired token")

```

### 在Web项目中的用法

```python
import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

# 导入配置文件中的密钥
from configs.server_config import SERVER_HOST, SERVER_PORT

app = FastAPI()

# 定义请求钩子，用于鉴权
async def authenticate(request: Request, call_next):
    try:
        # 从请求头部获取 Authorization 字段
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None:
            raise HTTPException(status_code=401, detail="缺少授权头部")

        # 检查 Authorization 字段是否以 Bearer 开头
        token_type, token = authorization_header.split()
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="无效的授权类型")

        # 解码 JWT
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        # 在 payload 中检查用户权限等信息，进行更详细的鉴权逻辑
        print(payload)

        # 调用下一个中间件或路由处理程序
        response = await call_next(request)
        return response

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="令牌已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的令牌")


# 注册请求钩子
app.middleware("http")(authenticate)


# 测试用法
# curl -X GET "http://127.0.0.1:7001" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTFiMmMzZDQiLCJleHAiOjE3MDkxMTMyNTh9.-s0DGfJrD6Xr417TzQK5-95vmyO6EnYNYoLzPXIC7zM""
@app.get("/")
async def root():
    # 访问根目录，默认跳转到SwaggerUI
    return RedirectResponse(url=f"http://{SERVER_HOST}:{SERVER_PORT}/docs/")


if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)

```

* * *

* * *

* * *

###### **基于[Jose4j](https://bitbucket.org/b_c/jose4j/wiki/JWT%20Examples "Jose4j")的JWT库，实现**

###### **[项目地址](https://gitee.com/eric-mao/test-jwt "项目地址")**

* * *

###### Demo.java

```java
import org.jose4j.jwa.AlgorithmConstraints;
import org.jose4j.jwk.RsaJsonWebKey;
import org.jose4j.jwk.RsaJwkGenerator;
import org.jose4j.jws.AlgorithmIdentifiers;
import org.jose4j.jws.JsonWebSignature;
import org.jose4j.jwt.JwtClaims;
import org.jose4j.jwt.MalformedClaimException;
import org.jose4j.jwt.consumer.ErrorCodes;
import org.jose4j.jwt.consumer.InvalidJwtException;
import org.jose4j.jwt.consumer.JwtConsumer;
import org.jose4j.jwt.consumer.JwtConsumerBuilder;
import org.jose4j.lang.JoseException;

import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.List;

public class Demo {

    /**
     * 创建 JWT
     *
     * @return jwt
     * @throws NoSuchAlgorithmException
     */
    private void createJWT() throws MalformedClaimException, JoseException {

        // 生成一个RSA密钥对，该密钥对将用于JWT的签名和验证，并封装在JWK中
        RsaJsonWebKey rsaJsonWebKey = RsaJwkGenerator.generateJwk(2048);
        // 给JWK一个密钥ID（kid），这只是礼貌的做法
        rsaJsonWebKey.setKeyId("k1");

        // 声明JWT，创建jwt具体内容
        JwtClaims claims = new JwtClaims();
        claims.setIssuer("Iss"); // 令牌的颁发者(谁创建的令牌)，其值是身份认证服务(OP)的URL
        claims.setAudience("Aud"); // 将令牌发送给谁，其值是三方软件(RP)的 app_id
        claims.setExpirationTimeMinutesInTheFuture(10); // 令牌的过期时间（10分钟后）
        claims.setGeneratedJwtId(); // 令牌的唯一标识符
        claims.setIssuedAtToNow(); // 颁发令牌的时间戳
        claims.setNotBeforeMinutesInThePast(2); // 令牌尚未生效的时间（2分钟前）
        claims.setSubject("subject"); // 令牌所涉及的主体/委托人
        claims.setClaim("email", "mail@example.com"); // 可以添加有关该主题的其他声明/属性
        List<String> groups = Arrays.asList("group-one", "other-group", "group-three");
        claims.setStringListClaim("groups", groups); // 支持多值声明，最终会成为一个JSON数组


        // JWT是以JSON声明作为有效负载的JWS和/或JWE。
        // 在本例中，它是一个JWS，因此我们创建了一个JsonWebSignature对象
        JsonWebSignature jws = new JsonWebSignature();

        // The payload of the JWS is JSON content of the JWT Claims
        // JWS 的payload JWT Claims 的 JSON 内容
        jws.setPayload(claims.toJson());

        // The JWT is signed using the private key
        // JWT签名使用的私钥
        jws.setKey(rsaJsonWebKey.getPrivateKey());

        // Set the Key ID (kid) header because it's just the polite thing to do.
        // We only have one key in this example but a using a Key ID helps
        // facilitate a smooth key rollover process
        // 设置密钥ID（kid）头，因为这只是礼貌之举。
        // 在本例中，我们只有一个密钥，但使用密钥ID有助于
        // 促进平稳的键翻转过程
        jws.setKeyIdHeaderValue(rsaJsonWebKey.getKeyId());

        // Set the signature algorithm on the JWT/JWS that will integrity protect the claims
        // 在JWT/JWS上设置签名算法，以保护声明的完整性
        jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.RSA_USING_SHA256);

        // Sign the JWS and produce the compact serialization or the complete JWT/JWS
        // representation, which is a string consisting of three dot ('.') separated
        // base64url-encoded parts in the form Header.Payload.Signature
        // If you wanted to encrypt it, you can simply set this jwt as the payload
        // of a JsonWebEncryption object and set the cty (Content Type) header to "jwt".
        // 签署JWS并生成紧凑的序列化或完整的JWT/JWS
        // 表示，它是由三个分隔的点（'.'）组成的字符串
        // 表单头中的base64url编码部分。有效载荷。签名
        // 如果您想对其进行加密，只需将此jwt设置为有效负载即可
        // 并将cty（内容类型）头设置为“jwt”。
        String jwt = jws.getCompactSerialization();


        // Now you can do something with the JWT. Like send it to some other party
        // over the clouds and through the interwebs.
        System.out.println("JWT: " + jwt);
        System.out.println("\n");


        // Use JwtConsumerBuilder to construct an appropriate JwtConsumer, which will
        // be used to validate and process the JWT.
        // The specific validation requirements for a JWT are context dependent, however,
        // it typically advisable to require a (reasonable) expiration time, a trusted issuer, and
        // and audience that identifies your system as the intended recipient.
        // If the JWT is encrypted too, you need only provide a decryption key or
        // decryption key resolver to the builder.
        // 使用JwtConsumerBuilder构造适当的JwtConsumer，它将用于验证和处理JWT。
        // 然而，JWT的具体验证要求取决于上下文，通常建议要求（合理的）到期时间、受信任的发行人和
        // 以及将您的系统标识为预期收件人的受众。
        // 如果JWT也是加密的，则只需提供解密密钥或
        // 将密钥解析程序解密到生成器。
        JwtConsumer jwtConsumer = new JwtConsumerBuilder()
                .setRequireExpirationTime() // JWT必须有一个到期时间
                .setAllowedClockSkewInSeconds(30) // 在验证基于时间的声明时，允许一些余地，以解释时钟偏移
                .setRequireSubject() // JWT必须有Subject声明
                .setExpectedIssuer("Iss") // JWT需要由谁签发。 (验证JWT的颁发者，是否一致)
                .setExpectedAudience("Aud") // JWT的目标对象是谁。(令牌发送给了谁，是否一致)
                .setVerificationKey(rsaJsonWebKey.getKey()) // 使用公钥验证签名
                .setJwsAlgorithmConstraints( // 仅允许给定上下文中的预期签名算法
                        AlgorithmConstraints.ConstraintType.PERMIT
                        , AlgorithmIdentifiers.RSA_USING_SHA256) // 这里只有RS256
                .build(); // 创建JwtConsumer实例

        try {
            //  验证 JWT 并将其转为 JwtClaims
            JwtClaims jwtClaims = jwtConsumer.processToClaims(jwt);
            System.out.println("JWT validation succeeded! " + jwtClaims);
        } catch (InvalidJwtException e) {
            // InvalidJwtException will be thrown, if the JWT failed processing or validation in anyway.
            // Hopefully with meaningful explanations(s) about what went wrong.
            System.out.println("Invalid JWT! " + e);

            // Programmatic access to (some) specific reasons for JWT invalidity is also possible
            // should you want different error handling behavior for certain conditions.

            // Whether or not the JWT has expired being one common reason for invalidity
            if (e.hasExpired()) {
                System.out.println("JWT expired at " + e.getJwtContext().getJwtClaims().getExpirationTime());
            }

            // Or maybe the audience was invalid
            if (e.hasErrorCode(ErrorCodes.AUDIENCE_INVALID)) {
                System.out.println("JWT had wrong audience: " + e.getJwtContext().getJwtClaims().getAudience());
            }
        }

    }

    public static void main(String[] args) throws NoSuchAlgorithmException, MalformedClaimException, JoseException {

        Demo test = new Demo();
        // 生成jwt串
        test.createJWT();

    }

}

```

* * *

* * *

* * *

##### **封装**

```java
import org.jose4j.jwa.AlgorithmConstraints;
import org.jose4j.jwk.RsaJsonWebKey;
import org.jose4j.jwk.RsaJwkGenerator;
import org.jose4j.jws.AlgorithmIdentifiers;
import org.jose4j.jws.JsonWebSignature;
import org.jose4j.jwt.JwtClaims;
import org.jose4j.jwt.MalformedClaimException;
import org.jose4j.jwt.consumer.ErrorCodes;
import org.jose4j.jwt.consumer.InvalidJwtException;
import org.jose4j.jwt.consumer.JwtConsumer;
import org.jose4j.jwt.consumer.JwtConsumerBuilder;
import org.jose4j.lang.JoseException;

import java.security.Key;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.util.Arrays;
import java.util.List;

public class Test {

    /**
     * KeyId
     */
    private String keyId;

    /**
     * 存放证书公钥
     */
    private PublicKey publicKey;

    /**
     * 存放证书私钥
     */
    private PrivateKey privateKey;

    /**
     * 证书长度 至少 1024, 建议 2048
     */
    private final int keySize = 2048;

    /**
     * 1. 模拟生成证书
     *
     * @throws JoseException
     */
    private void createKeyPairGenerator() throws NoSuchAlgorithmException, JoseException {

        // 生成一个RSA密钥对，该密钥对将用于JWT的签名和验证，并封装在JWK中
        RsaJsonWebKey rsaJsonWebKey = RsaJwkGenerator.generateJwk(keySize);
        // 给JWK一个密钥ID（kid），这只是礼貌的做法
        keyId = "k1-RsaJsonWebKey";
        publicKey = rsaJsonWebKey.getRsaPublicKey();
        privateKey = rsaJsonWebKey.getRsaPrivateKey();

//        // 另一种生成证书的方法
//        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
//        keyPairGenerator.initialize(keySize);
//        KeyPair keyPair = keyPairGenerator.genKeyPair();
//        keyId = "k1-KeyPairGenerator";
//        publicKey = keyPair.getPublic();
//        privateKey = keyPair.getPrivate();
    }

    /**
     * 2. 创建JWT Header
     *
     * @param jws
     */
    private void createHeader(JsonWebSignature jws) {

        // JWT第1部分. 头部Header
        jws.setKeyIdHeaderValue(keyId);
        // JWT第1部分. 头部Header
        jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.RSA_USING_SHA256);
    }

    /**
     * 3. 创建JWT Payload
     *
     * @return
     */
    private String createPayload() {

        // 声明JWT，创建jwt具体内容
        JwtClaims claims = new JwtClaims();
        claims.setIssuer("Iss"); // 令牌的颁发者(谁创建的令牌)，其值是身份认证服务(OP)的URL
        claims.setAudience("Aud"); // 将令牌发送给谁，其值是三方软件(RP)的 app_id
        claims.setExpirationTimeMinutesInTheFuture(10); // 令牌的过期时间（10分钟后）
        claims.setGeneratedJwtId(); // 令牌的唯一标识符
        claims.setIssuedAtToNow(); // 颁发令牌的时间戳
        claims.setNotBeforeMinutesInThePast(2); // 令牌尚未生效的时间（2分钟前）
        claims.setSubject("subject"); // 令牌所涉及的主体/委托人
        claims.setClaim("email", "siyu.mao@dhc.com.cn"); // 可以添加有关该主题的其他声明/属性
        List<String> groups = Arrays.asList("group-one", "other-group", "group-three");
        claims.setStringListClaim("groups", groups); // 支持多值声明，最终会成为一个JSON数组

        return claims.toJson();
    }

    /**
     * 4. 创建JWT Signature
     *
     * @param jws
     */
    private void createSignature(JsonWebSignature jws) {

        // JWT第3部分. 使用私钥生成JWT的签名
        jws.setKey(privateKey);
    }

    /**
     * 4. 创建JWT
     *
     * @return
     * @throws JoseException
     */
    private String createJWT() throws JoseException {

        // JWT是以JSON声明作为有效负载的JWS和/或JWE。
        // 在本例中，它是一个JWS，因此我们创建了一个JsonWebSignature对象
        JsonWebSignature jws = new JsonWebSignature();
        // JWT第1部分. 生成Header
        this.createHeader(jws);
        // JWT第2部分. 生成Payload
        jws.setPayload(this.createPayload());
        // JWT第3部分. 生成Signature
        this.createSignature(jws);

        // 将jws转为 jwt串
        String jwt = jws.getCompactSerialization();
        System.out.println("JWT:");
        System.out.println("\t" + jwt);
        System.out.println("\n");
        return jwt;
    }

    /**
     * 验证签名使用的公钥
     *
     * @param jwt
     * @param verificationKey
     * @throws MalformedClaimException
     */
    private void validateJWT(String jwt, Key verificationKey) throws MalformedClaimException {

        // 使用JwtConsumerBuilder构造适当的JwtConsumer，它将用于验证和处理JWT。
        // 然而，JWT的具体验证要求取决于上下文，通常建议要求（合理的）到期时间、受信任的发行人和
        // 以及将您的系统标识为预期收件人的受众。
        // 如果JWT也是加密的，则只需提供解密密钥或
        // 将密钥解析程序解密到生成器。
        JwtConsumer jwtConsumer = new JwtConsumerBuilder()
                .setRequireExpirationTime() // JWT必须有一个到期时间
                .setAllowedClockSkewInSeconds(30) // 在验证基于时间的声明时，允许一些余地，以解释时钟偏移
                .setRequireSubject() // JWT必须有Subject声明
                .setExpectedIssuer("Iss") // JWT需要由谁签发。 (验证JWT的颁发者，是否一致)
                .setExpectedAudience("Aud") // JWT的目标对象是谁。(令牌发送给了谁，是否一致)
                .setVerificationKey(verificationKey) // 使用公钥验证签名
                .setJwsAlgorithmConstraints( // 仅允许给定上下文中的预期签名算法
                        AlgorithmConstraints.ConstraintType.PERMIT
                        , AlgorithmIdentifiers.RSA_USING_SHA256) // 这里只有RS256
                .build(); // 创建JwtConsumer实例

        try {
            //  验证 JWT 并将其转为 JwtClaims
            JwtClaims jwtClaims = jwtConsumer.processToClaims(jwt);
            System.out.println("JWT 验证成功 :-)");
            System.out.println("Payload:");
            System.out.println("\t" + jwtClaims.toJson());
            System.out.println("\n");
        } catch (InvalidJwtException e) {

            // 如果JWT处理或验证失败，将抛出InvalidJwtException。
            System.out.println("JWT 验证失败 :-(");

            // 还可以根据错误码来进一步的了解异常原因
            JwtClaims jwtClaims = e.getJwtContext().getJwtClaims();
            // JWT已经过期
            if (e.hasExpired()) {
                System.out.println("\t JWT已经过期: " + jwtClaims.getExpirationTime());
            }

            // JWT的Audience无效
            if (e.hasErrorCode(ErrorCodes.AUDIENCE_INVALID)) {
                System.out.println("\t JWT的Audience值无效: " + jwtClaims.getAudience());
            }

            // JWT的Issuer无效
            if (e.hasErrorCode(ErrorCodes.ISSUER_INVALID)) {
                System.out.println("\t JWT的Issuer值无效: " + jwtClaims.getIssuer());
            }

        }
    }

    /**
     * 入口
     *
     * @param args
     * @throws MalformedClaimException
     * @throws JoseException
     */
    public static void main(String[] args) throws MalformedClaimException, JoseException, NoSuchAlgorithmException {

        Test test = new Test();
        // 创建证书
        test.createKeyPairGenerator();
        // 生成jwt串
        String jwt = test.createJWT();
        // 验证jwt串
        test.validateJWT(jwt, test.publicKey);

    }

}

```

* * *

* * *

* * *

###### pom.xml

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>TestJWT</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.bitbucket.b_c</groupId>
            <artifactId>jose4j</artifactId>
            <version>0.7.9</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>1.7.25</version>
            <scope>compile</scope>
        </dependency>
    </dependencies>

</project>
```

* * *

* * *

* * *
