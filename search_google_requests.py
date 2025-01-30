import requests
import urllib.parse
from bs4 import BeautifulSoup

import requests

def google_search(query, num_results=5):
    query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    
    headers = {
        "Host": "www.google.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Alt-Used": "www.google.com",
        "Connection": "keep-alive",
        "Cookie": "SOCS=CAISNQgCEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjQxMjE3LjA1X3AwGgJwbCAEGgYIgMXHuwY; NID=521=uNr8Gf5ndEmAVmUuZesueVvFLrynWYYOLouZlpiASOL69Hj1e8KeDc2URkfoc5uzTyO3R-euaGQ3noTmx21NDIMKoGXotjLXNfjsXe0swrV5H_5BcYCGMYJRV4ifnW99pzW8kfanRrOu1OMcg9npNacOQg04n1p3jPFejI_SzghsRShvYgkHiPvmlAhFGRkPSfsNKMI2px9mLZ8eeIYmGuXOjKxzV6hNq660W5MNPk49wZYQk9yClM6IsXEv2IP0MWqGmny3vT3Lyc_ch7ZrDMQjYN-FqKbsgLIU-_BB5nvi-KK6_VLHwbt41xra1HnaRWDiHigcoycST4ALliqE69StYvsS809Rzf9Oku1x5qYZUhoYAKF9Be_EKxe8_m3u3W3oTzu6xUG4EQ4BbZ-X2BdvFwO4r5pM8icSzGU1nvX1Gbp9ObWxkgNCNG1tqXFj4RYaTT7wuRPWgLe8R1pH2j_16yOssc9l1kTiOu6jhT6RQVJFduKf9Us; SID=g.a000swjwSpTThrc3qKF-pw1ndv8UgaIP1xvOH5Q9PKHY4aLiXzP9zEe5OFCm9fnWpa8enrzMpwACgYKARkSARESFQHGX2MigJIHjPFI_SsPA4fYXcYphBoVAUF8yKq9hjDrMauCQa5Ib4TTdNIZ0076; __Secure-1PSID=g.a000swjwSpTThrc3qKF-pw1ndv8UgaIP1xvOH5Q9PKHY4aLiXzP9uPS05liyj4nG86GN7r3_7wACgYKAZgSARESFQHGX2Miq7KEBXYOwJ9RWVDC1AhkSRoVAUF8yKrEQrkxm-RxOF9qJ6MtmMKh0076; __Secure-3PSID=g.a000swjwSpTThrc3qKF-pw1ndv8UgaIP1xvOH5Q9PKHY4aLiXzP9UMA1Xozewjgz1lS-CkXRWQACgYKAfcSARESFQHGX2MiqzSNY0ySPegb31khQHoHiRoVAUF8yKpakupUANATNQIVD8lXZEa_0076; HSID=AoEDXF8CpPd8Dp1Sr; SSID=AkGLtCMUMOjRVBNhn; APISID=eeslNkFQ4HGa8z6_/A7CwuLbIo4aesdSs1; SAPISID=lpuq3vlcaxlTiig3/AAceZSj2whfTPPZqR; __Secure-1PAPISID=lpuq3vlcaxlTiig3/AAceZSj2whfTPPZqR; __Secure-3PAPISID=lpuq3vlcaxlTiig3/AAceZSj2whfTPPZqR; SIDCC=AKEyXzVLQLmr_T6cdrY__UAnQqgGnI9CEM4m_2bvTxv9BZY9qAbI2vMMcpzsI43v45r_-em4ddg; __Secure-1PSIDCC=AKEyXzWmwsHesnTiKc_3Wlg_UvA1nvXczoCUD0Z5U-PGNyWwfTgYmJ9vZSzFWnP9OQuyhqv5SvA; __Secure-3PSIDCC=AKEyXzVa8Kuxj9pRAPozyz_Rks43AAv2QvN1GSDyiKyVnj-Jy-u6KWm7SwiwkctfJ_OLQbFY-to_; SEARCH_SAMESITE=CgQIkJ0B; __Secure-1PSIDTS=sidts-CjEBmiPuTVbw729tg_ktm8K9XUgeMuEE9NFyhTssqnO19_2GcxphrJe_6fTCK_CsuXsXEAA; __Secure-3PSIDTS=sidts-CjEBmiPuTVbw729tg_ktm8K9XUgeMuEE9NFyhTssqnO19_2GcxphrJe_6fTCK_CsuXsXEAA; AEC=AZ6Zc-X9nBfSx-l0v-mpNtlnpi08OE9WaOgYSS5KfGMcagvTN4sUds8l6Io; OTZ=7885298_52_52_123900_48_436380; S=billing-ui-v3=VfjxtJLXbASZuBrPKu0VZLYY0vGYDlWn:billing-ui-v3-efe=VfjxtJLXbASZuBrPKu0VZLYY0vGYDlWn; DV=sy6ocwaeCV9WsO9g7sjbrkeqrkLpSVnjuvLUHP2URQEAAFDnUmPnDIwfagAAAGC9VCFbQNaLMwAAAIQQ4-QFXGMHDgAAAA",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open("page.html", "w") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    
    search_results = soup.select("div.yuRUbf a")
    links = [result["href"] for result in search_results[:num_results]]
    
    return links

if __name__ == "__main__":
    query = "Python Selenium tutorial"
    results = google_search(query)

    print("Wyniki wyszukiwania:")
    for index, link in enumerate(results, start=1):
        print(f"{index}. {link}")
