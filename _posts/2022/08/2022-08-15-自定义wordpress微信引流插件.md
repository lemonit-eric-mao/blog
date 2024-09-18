---
title: "自定义wordpress微信引流插件"
date: "2022-08-15"
categories: 
  - "wordpress"
---

###### 创建文件 **wechat-pilotflow.php**

```php
<?php
/**
 * Plugin Name: 微信关注引流插件
 * Version: 0.1.0
 * Author: Eric.Mao
 * Author URI: http://www.dev-share.top
 */
error_reporting(E_ERROR | E_PARSE);
ob_start();
register_activation_hook(__FILE__, 'pilotflow_install');

register_deactivation_hook(__FILE__, 'pilotflow_remove');

function pilotflow_install()
{
    add_option("pilotflow", "", '', 'yes');
}

function pilotflow_remove()
{
    delete_option('pilotflow');
}

if (is_admin()) {
    add_action('admin_menu', 'pilotflow_menu');
}

function pilotflow_menu()
{
    add_options_page('Wechat pilotflow', '微信公众号引流设置', 'administrator', 'pilotflow', 'pilotflow_html_page');
}

add_action('plugin_action_links_' . plugin_basename(__FILE__), 'pilotflow_plugin_actions');
function pilotflow_plugin_actions($links)
{
    $new_links = array();
    $new_links[] = '<a href="admin.php?page=pilotflow">设置</a>';
    return array_merge($new_links, $links);
}

function pilotflow_html_page()
{
    ?>
    <div>
        <h2>微信公众号设置</h2>
        <form method="post" action="options.php" style="margin: 0;">

            <?php wp_nonce_field('update-options');
            $pilotflow = get_option('backend_pilotflow');
            ?>
            <p>
                <strong>微信公众号名称：</strong><br/>
                名称：<input name="backend_pilotflow[wechat_name]" type="text" value="<?php echo isset($pilotflow['wechat_name']) ? $pilotflow['wechat_name'] : '微信关注引流插件'; ?>"/>
                微信公众号平台→公众号设置→名称
            </p>
            <p>
                <strong>微信公众号：</strong><br/>
                微信号：<input name="backend_pilotflow[wechat_account]" type="text" value="<?php echo isset($pilotflow['wechat_account']) ? $pilotflow['wechat_account'] : 'soft-tech-share'; ?>"/>
                微信公众号平台→公众号设置→微信号
            </p>
            <p>
                <strong>回复以下关键词获取验证码：</strong><br/>
                关键词：<input name="backend_pilotflow[wechat_keyword]" type="text" value="<?php echo isset($pilotflow['wechat_keyword']) ? $pilotflow['wechat_keyword'] : '验证码'; ?>"/>
                微信验证码，访客回复这个关键词就可以获取到验证码
            </p>
            <p>
                <strong>需要用户输入的验证码：</strong><br/>
                验证码：<input name="backend_pilotflow[wechat_code]" type="text" value="<?php echo isset($pilotflow['wechat_code']) ? $pilotflow['wechat_code'] : '666'; ?>"/>
                该验证码要和微信公众号平台自动回复的内容一致，最好定期两边都修改下
            </p>
            <p>
                <strong>微信公众号二维码地址：</strong><br/>
                图片地址：<input name="backend_pilotflow[wechat_qrimg]" style="width:400px;" type="text" value="<?php echo isset($pilotflow['wechat_qrimg']) ? $pilotflow['wechat_qrimg'] : 'http://qiniu.dev-share.top/image/jpg/soft-tech-share.jpg'; ?>"/>
                填写您的微信公众号的二维码图片地址
            </p>
            <p>
                <strong>Cookie有效期：</strong><br/>
                有效天数：<input name="backend_pilotflow[wechat_day]" type="text" value="<?php echo isset($pilotflow['wechat_day']) ? $pilotflow['wechat_day'] : '7'; ?>"/>天，
                在有效期内，访客无需再获取验证码可直接访问隐藏内容
            </p>
            <p>
                <strong>加密密钥：</strong><br/>
                密钥：<input name="backend_pilotflow[wechat_key]" type="text"
                          value="<?php echo isset($pilotflow['wechat_key']) ? $pilotflow['wechat_key'] : md5('dev-share.top' . time() . rand(10000, 99999)); ?>"/>
                用于加密Cookie，默认是自动生成，一般无需修改，如果修改，所有访客需要重新输入验证码才能查看隐藏内容
            </p>
            <p>
                <strong>锁定状态下的文本：</strong><br/>
                文本：<input name="backend_pilotflow[wechat_lock_text]" type="text" value="<?php echo isset($pilotflow['wechat_lock_text']) ? $pilotflow['wechat_lock_text'] : '关注后解锁'; ?>"/>
            </p>

            <p>
                <input type="hidden" name="action" value="update"/>
                <input type="hidden" name="page_options" value="backend_pilotflow"/>
                <input type="submit" value="保存" class="button-primary"/>
            </p>
        </form>
    </div>
    <?php

}

add_filter('the_content', 'backend_wechat_pilotflow');
function backend_wechat_pilotflow($content)
{
    $cookie_name = 'backend_wechat_pilotflow';

    if (preg_match_all('/<!--hide start-->([\s\S]*?)<!--hide end-->/i', $content, $hide_words)) {
        $pilotflow = get_option('backend_pilotflow');
        $cv = md5($pilotflow['wechat_key'] . $cookie_name . 'dev-share.top');
        $vtips = '';
        // 判断是否已经输入了验证码
        if (isset($_POST['backend_verifycode'])) {
            // 判断输入的验证是否正确
            if ($_POST['backend_verifycode'] == $pilotflow['wechat_code']) {
                setcookie($cookie_name, $cv, time() + (int)$pilotflow['wechat_day'] * 86400, "/");
                $_COOKIE[$cookie_name] = $cv;
            } else {
                // 验证码输入错误，提示框
                $vtips = '<script>alert("验证码错误！请输入正确的验证码！");</script>';
            }
        }
        $cookievalue = isset($_COOKIE[$cookie_name]) ? $_COOKIE[$cookie_name] : '';

        // 验证码【正确】时显示内容
        if ($cookievalue == $cv) {
            // 如果验证码存在，将显示所有数据内容
            $html = '
                <div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">
                   <hr style="border:1px dashed #F60;"/>
                   <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span>
                </div>
                ' . $hide_words[0][0];
            $content = str_replace($hide_words[0], $html, $content);
        } else {
            // 验证码【不正确】时显示内容
            $hide_notice = '
                <script>
                    function pop_show() {
                        document.getElementById("pop").style.display = "block";
                    }
                    function pop_hide() {
                        document.getElementById("pop").style.display = "none";
                    }
                </script>

                <!-- 显示弹窗 -->
                <span onclick="pop_show();"
                      style="cursor: pointer; text-align: center; display: block; color: #c00; background-color: white; background-image: url(http://qiniu.dev-share.top/image/png/ico_lock.png); background-size: 17px; background-repeat: no-repeat; background-position: 42% 50%;">
                      ' . $pilotflow['wechat_lock_text'] . '
                </span>

                <!-- 弹窗 -->
                <div id="pop" onclick="pop_hide();"
                     style="display: none;background: rgba(52, 58, 65, 0.600000);backdrop-filter: blur(4px);-webkit-backdrop-filter: blur(4px);position: fixed;z-index: 10;top: 0;left: 0;width: 100%;height: 100%;">
                    <div id="pop_body" onclick="event.stopPropagation();"
                         style="position: absolute;top: 25%;left: 50%;margin-left: -18rem;background: rgba(255, 255, 255, 1);box-shadow: 0px 8px 12px rgba(60 64 67 .15), 0px 4px 4px rgba(60 64 67 .3);width: 36rem;height: 24rem;border-radius: 0.3rem;">
                        <h6 style="display: flex;justify-content: space-between;align-items: center;font-weight: 500;font-size: 1.25rem;padding: 10px;border-bottom: 1px solid #ccc;margin: 0;">
                            ' . $pilotflow['wechat_name'] . '
                            <span onclick="pop_hide();"
                                  style="color: #999;font-size: .8rem;font-weight: normal;cursor: pointer;">关闭</span>
                        </h6>
                        <div class="pd-1" style="padding: 1rem; background-color: white;">
                            <div style="text-align: center;">
                                <img src="http://qiniu.dev-share.top/image/png/ico_wx.png" style="width:20px;height:20px;">
                                <span style="font-weight: 500; font-size: 17px;">
                                    扫码关注<em style="font-style: normal;padding: 0 0.25rem;color: #f60;">1秒</em>登录
                                </span>
                            </div>
                            <div style="text-align: center;">
                                <img src="' . $pilotflow['wechat_qrimg'] . '" alt="' . $pilotflow['wechat_name'] . '"
                                     style="width:150px;height:150px;">
                            </div>
                            <div style="margin-top:10px;display:flex;justify-content: center;">
                                <form method="post">
                                    <div style="display:flex;justify-content: center;align-items: center;">
                                        <input name="backend_verifycode" id="verifycode" type="password" value="" autocomplete="off" placeholder="输入验证码"
                                               style="border: 1px solid #01a05c;height: 3rem; width: 15rem; font-size: 1rem;border-radius: 4px 0 0 4px;">
                                        <input id="verifybtn" name="" type="submit" value="GO"
                                               style="border: 0;background: #01a05c;color: white;font-size: 1rem;padding: 0.5rem 0.8rem;border-radius: 0 4px 4px 0;cursor: pointer;">
                                    </div>
                                </form>
                            </div>
                            <div class="center" style="justify-content: center; display: flex; margin: 4px; font-size: .8rem; color: #f60;">
                                发送 "' . $pilotflow['wechat_keyword'] . '" 获取
                                <em style="padding: 0 .5rem;">|</em>
                                <span style="color: #01a05c;">' . $pilotflow['wechat_day'] . '天全站免登陆</span>
                            </div>
                            <div style="position: absolute;bottom: 0;background: #a10000;display: block;border-radius: 0 0 4px 4px;color: white;opacity: .7;left: 0;text-align: center;width: 100%;line-height: 2rem;font-size: .9rem;"></div>
                        </div>
                    </div>
                </div>
                '
                . $vtips;
            $content = str_replace($hide_words[0], $hide_notice, $content);
        }

    }
    return $content;
}

add_action('admin_footer', 'backend_wechat_pilotflow_toolbar');
function backend_wechat_pilotflow_toolbar()
{
    if (!strpos($_SERVER['SCRIPT_NAME'], 'post.php') && !strpos($_SERVER['SCRIPT_NAME'], 'post-new.php')) {
        return '';
    }
    global $wp_version;
    $pilotflow_271_hacker = ($wp_version == '2.7.1') ? ".lastChild.lastChild" : "";
    ?>
    <script type="text/javascript">
        jQuery(document).ready(function ($) {
            <?php if ( version_compare($GLOBALS['wp_version'], '3.3alpha', '>=') ) : ?>
            edButtons[edButtons.length] = new edButton(
                // id, display, tagStart, tagEnd, access_key, title
                "pilotflow", "插入微信隐藏标签", "<!--hide start-->", "<!--hide end-->", "h", "插入微信隐藏标签"
            );
            <?php else : ?>
            if (s2v_toolbar = document.getElementById("ed_toolbar")<?php echo $pilotflow_271_hacker ?>) {
                pilotflowNr = edButtons.length;
                edButtons[pilotflowNr] =
                    new edButton('pilotflow', '插入微信隐藏标签', '<!--hide start-->', '<!--hide end-->', 'h', "插入微信隐藏标签"
                    );
                var pilotflowBut = s2v_toolbar.lastChild;

                while (pilotflowBut.nodeType != 1) {
                    pilotflowBut = pilotflowBut.previousSibling;
                }

                pilotflowBut = pilotflowBut.cloneNode(true);
                pilotflowBut.value = "pilotflow";
                pilotflowBut.title = "插入微信隐藏标签";
                pilotflowBut.onclick = function () {
                    edInsertTag(edCanvas, parseInt(pilotflowNr));
                }
                s2v_toolbar.appendChild(pilotflowBut);
                pilotflowBut.id = "pilotflow";
            }
            <?php endif; ?>
        });
    </script>
<?php } ?>
```

**只需要将文件打包成`wechat-pilotflow.zip`格式即可`上传到wordpress`插件中使用**

* * *

###### **[具体使用参考链接](docker-compose-%e5%ae%89%e8%a3%85-wordpress "具体使用参考链接")**
