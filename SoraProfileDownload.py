import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# CONFIG
PROFILE_URL = "https://sora.chatgpt.com/profile/illphated1"
OUTPUT_DIR = "sora_videos"
COOKIE_VALUE = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..5b5wawA9Wpsz4OHA.gioxvfjb8hDyJiAQfAdgOwScYyTNLWO12J8RGow5-VO8lcP9EFQTMSGqLFsrNSewsdBYSIUEY4rE56he4Fcu32w5jyT2fFWW2EAeKXR7uJ8VrxiW1L0S6Zh76U3CfRUHADfxMWM9QkO_S2c9qNQOeXzLrQ0Z4IEBsEOX-jaJUu_BM8qoL89uN3KWiLUlGltxmPS813OgESrQS3avXqafihEWMIX34qO0prbIY-Rw6dyRDpmBV_BO2ttuC0kMVTyjLDSin1PCtUDuDwJAbr-15hOjckM7BhKtD-0FO-OS5F2IOPMjfTXCH4Ts7EAY4fufaCYlWwwZgr-oLawPdbMwiTazqB0ajUDxoI-7Ne7Lf2oASaTFp5PVK-tBWdO6PQI6ZYmGoG8GeVEyzLNsm7t6Q0Ba0tYVCj2Y5SZWMVah6mwS5p0CcHzrQVOJA--Rm93kgNKBYvSCn6aKa4h5Dmkljq9lzjWStX8FkNqB4X9Bhhc8_2DRGdafnFNR_E73hIaEviX8C2dxS7sDT7xB2t9dOfcPmcefvfTv5MU0ulKwmAe1gj3mpj3vjdZDhiTbLMgVznCNSR9g-v5EA9AVU6F_mDH4oslRJ18FFLT1fCe8UdcemV1MkeGALwjWzWUufCfjJChm__B_A1am5qHhusHDfuIV7b2nO83_pZYQ3Fxs3TzexiE7VnnkHppN6CeY39lAdUALts1in2FylqDagoZC040axdCPr-bb9T_cbMOG5Gjp2J7vjR0BdnRhCELsAeaUlEO_lvE8U_GxGigipQQPTIa_hLIprNuaiVGJRSt5w5osYMJBsBPbgYykEF11lclB35OWSzdjUKbCTpVWNsAzuorOkUnRQsFMmdIkpSWPJuMvlxdMnZO36VIPyK8L4TcS9qnCfCrwx8o3QSTVlkfIxQ-p08-H8yCyFqrE12jtdseyFV2Ao3gjav7oaE89RtT5bklhcuHZeVtyqD5ij0SqK3d4pENQVh7F_0DxrOG5eQLrJbnOx4mbfLzMEYPs6Ux7ftU99bFW5KfJrJi2PVYpT0_BDmxeLKYoR1Xy8M12Imek25VZpSlhQoEcyOXbKFztoCwP8mPdbeboBX88IU-lvhdpM5hFVq00XcJoi0GyP0g6ERKRv1COgSKRSQqI8JCuHKDDHvxOxUc87JyOVoVGJxb0W3qJA8UiFRVOZKhGLdcBv3ay-bEpYlbbOCRO2Zq8n3Djceo_3YFUrm3BGtQ67tGXwN28Yqo2GmYblFXpoyNRZ0UmxGhGo55OoH58YOwBhHa488AribXtVpUetWBf8QB7cNvy8R6sUk5qI1GZBKdNiDXtbWjSt72GQbDOHvAZsOeYlmWIf3ywlyrcboxmzeaLtDzzn0pvUjyfcEXYDHJNRQsB-kz2JoBkT37bHPOxNKnnuYq5hEIjHUDNpATRgm0lmz5y2JPUar5OCH3K0QBhccd_zCRKJK6dEpkGkDoTzZdzjbvRHALa9vL7e-tn4VOd0O2CVDPmCz9k0KJXpUL7-qGqkbwTwuWI9wLYOO7xjqXxQ5jOFnP5XgL0gmBh-pgXgF2TZYe3HA9D24g1feyNGd1FWja5MbB8kaPTF3a0Z3dPb9eLoIEKllRA28NO-PcFl9D4fRUGHPcDqIIHfgIIDGph0Xm5Y7cSBkRCydv-Z9bPO6NyN1aIQBip9IqCe94yYHgEZNBOnq4BoPi_KHiopGwjmoRNM_MPb0yEfP45mLO4KDbWiON_tF00tdptUUuOtes916pzz1-aDxRIkJYa0KK-dnyk5doM1ZahgW7GG0Kt8QiVKA2vO7_gebgB0W-ShJV0G96khhbBRgWWkgSIrlPgt9e5SY2bXB9Vy-xMgrVhmGz6iiv9qD7aBMStHpacRWm9uXJiGoJ5pROK_t-zS10BpI96V-wKVojfm1g_qjL_ycc7jTsQLEeTBrh8hTnpuoe-gVqKaPUOdBf6jvO6_bIKygCj5WSqJCmVE77Z2qj6HWhwV1IOxK7l3-knlt6UdKck5kUYmhAgmQgyxwvG93yuEs3O9EMBY32krMxNHaTyFfvPUQwu3e1VRp3k1TqA5wtWcxu9ES_DuoQCTB-qurjDSaiRo6HQ6D9Cna4zhuW49GVhc1Cz8zYrL5bnGXb4BObcCNGf7x9Ypz4pWVO9knKYB7jSQfrHeb-HoAf8jghXLnv_i18WMP4kMJu-AVVlGun7dDi7qmjYFFrQZ7rsmZaD2abFcuBU0ihvZICm6Q9VNNQRLY9DWdWTaB0U4CqgjwATpVD4LcErpT3DJNYxt2vXDTXr1KMbnh93Ozif3k4rXSu4VDm8olD2fqb70-nHX1MPBubf7Oe8lG-45ffLiJ2xRVPwol7gvclWNH1_53B0suhANbau4fROtjNDP_pxkvScNTnwKJrmzeKyAa7pr3OTUSIDvwHYqirvOq52kRPWcmtDIrYQitmUIMIzQcOvUiOMb33cejGkJ8b4_6lIWeilWKsD-7iqN8PQ8PG0mfywhsW2dFgbHJCT_nSUzNT2Ge9-Vm9XUOJKLGkTqTuFUYw63O719CQ0PU8lJKynyfsunCw5hFhzqUrmGQ8H4R-QIOJOfgInpNM5Uwp2xUy6vR4lar9SONLQrcROLoVcFKlvL"

def download_video(url, folder):
    filename = url.split("?")[0].split("/")[-1]
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath):
        print(f"Skipping {filename} (Exists)")
        return
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(1024*1024):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Setup Chrome Browser
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Uncomment this to run invisible
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("Opening browser...")
        # 2. Go to domain first so we can set cookies
        driver.get("https://sora.chatgpt.com")
        
        # 3. Add the authentication cookie
        print("Setting cookies...")
        driver.add_cookie({
            'name': '__Secure-next-auth.session-token',
            'value': COOKIE_VALUE,
            'domain': '.sora.chatgpt.com',
            'path': '/',
            'secure': True
        })

        # 4. Refresh and go to profile
        print(f"Navigating to {PROFILE_URL}")
        driver.get(PROFILE_URL)

        # 5. Wait specifically for VIDEO tags to appear
        print("Waiting for videos to load...")
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
        except:
            print("Timeout: No videos found immediately. Proceeding anyway.")

        # 6. Scroll down to trigger lazy loading (Sora uses infinite scroll)
        print("Scrolling to load more videos...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3): # Increase range to scroll more
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 7. Extract URLs
        print("Extracting URLs...")
        video_elements = driver.find_elements(By.TAG_NAME, "video")
        video_urls = set()
        
        for v in video_elements:
            src = v.get_attribute("src")
            # Sometimes videos have a <source> child instead of src attribute
            if not src:
                sources = v.find_elements(By.TAG_NAME, "source")
                for source in sources:
                    src = source.get_attribute("src")
                    if src: break
            
            if src and src.startswith("http"):
                video_urls.add(src)

        print(f"Found {len(video_urls)} unique videos.")
        
        # 8. Download
        for url in video_urls:
            download_video(url, OUTPUT_DIR)

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()