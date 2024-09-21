from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

def guess_the_pin(start_key, end_key):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.guessthepin.com/")
    key = start_key
    print(f"Starting from {start_key} to {end_key}")

    while key <= end_key:
        try:
            input_box = driver.find_element(By.NAME, "guess")
            submit_button = driver.find_element(
                By.XPATH, '//*[@id="container"]/form/input[2]'
            )

            input_box.send_keys(str(key).zfill(4))
            if key % 100 == 0:
                print(f"Trying key: {key}")
            submit_button.click()

            driver.implicitly_wait(0.1)
            p_tag = driver.find_element(By.XPATH, '//*[@id="container"]/form/p')
            if "incorrectly" not in p_tag.text:
                print("Key found:", key)
                driver.quit()
                return key
        except Exception as e:
            print(f"An error occurred: {e}")
            driver.refresh()

        key += 1

    driver.quit()
    return None


if __name__ == "__main__":
    num_chunks = 10
    chunk_size = 1000
    with ThreadPoolExecutor(max_workers=num_chunks) as executor:
        futures = [
            executor.submit(
                guess_the_pin, i * chunk_size, min((i + 1) * chunk_size - 1, 9999)
            )
            for i in range(num_chunks)
        ]

    for future in futures:
        result = future.result()
        if result:
            print(f"Final result: {result}")
            break
