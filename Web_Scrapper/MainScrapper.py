from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def webListings():
    service = Service(executable_path=r'input_driver_path')
    driver = webdriver.Chrome(service=service)
    driver.get(
        "input_web_url")   # URL to be scrapped

    # Wait for the 'shimmer-container' elements to be loaded
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'shimmer-container')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    response = soup.find_all('div', class_='shimmer-container')

    hrefs = []

    for item in response:
        a_tag = item.find('a', class_='btn-bg')
        if a_tag and 'href' in a_tag.attrs:
            href = a_tag['href']
            hrefs.append(href)

    # Base URL for the website
    base_url = "https://portal.onehome.com"

    data = []

    for href in hrefs:
        driver.get(base_url + href)
        # Wait for the necessary element to be loaded in the new page
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sold-price')))
        listing_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract the sell price correctly
        sold_price_div = listing_soup.find('div', class_='sold-price')
        listed_for_spans = sold_price_div.find_all('span', class_='listed-for') if sold_price_div else []

        list_price = None
        if len(listed_for_spans) > 1:
            list_price = listed_for_spans[1].text.strip()

        structure_type_li = listing_soup.find('li', {'class': 'feature', 'data-qa': 'StructureTypeColon-feature'})
        structure_type = structure_type_li.find('dd', class_='detail').text.strip() if structure_type_li else None

        property_type_dt = listing_soup.find('dt', text='Property Type')
        property_type = property_type_dt.find_next_sibling('dd', class_='detail').text.strip() if property_type_dt else None

        beds_dt = listing_soup.find('dt', text='Beds')
        beds = beds_dt.find_next_sibling('dd', class_='detail').text.strip() if beds_dt else None

        full_baths_dt = listing_soup.find('dt', text='Full Bathrooms')
        full_baths = full_baths_dt.find_next_sibling('dd', class_='detail').text.strip() if full_baths_dt else None

        half_baths_dt = listing_soup.find('dt', text='Half Bathrooms')
        half_baths = half_baths_dt.find_next_sibling('dd', class_='detail').text.strip() if half_baths_dt else '0'

        square_footage_dt = listing_soup.find('dt', text='Size')
        square_footage = square_footage_dt.find_next_sibling('dd', class_='detail').text.strip() if square_footage_dt else None

        lot_size_dt = listing_soup.find('dt', text='Lot Size Area')
        lot_size = lot_size_dt.find_next_sibling('dd', class_='detail').text.strip() if lot_size_dt else None

        hoa_fee_dt = listing_soup.find('dt', text='HOA Fee:')
        hoa_fee = hoa_fee_dt.find_next_sibling('dd', class_='detail').text.strip() if hoa_fee_dt else '0'

        parking_spots_dt = listing_soup.find('dt', text='Parking Spots:')
        parking_spots = parking_spots_dt.find_next_sibling('dd', class_='detail').text.strip() if parking_spots_dt else '0'

        garage_spaces_dt = listing_soup.find('dt', text='Garage Spaces:')
        garage_spaces = garage_spaces_dt.find_next_sibling('dd', class_='detail').text.strip() if garage_spaces_dt else '0'

        closed_on_dt = listing_soup.find('dt', text='Closed On:')
        closed_on = closed_on_dt.find_next_sibling('dd', class_='detail').text.strip() if closed_on_dt else None

        stories_dt = listing_soup.find('dt', text='Stories')
        stories = stories_dt.find_next_sibling('dd', class_='detail').text.strip() if stories_dt else '0'

        style_dt = listing_soup.find('dt', text='Style')
        style = style_dt.find_next_sibling('dd', class_='detail').text.strip() if style_dt else None

        attached_garage_dt = listing_soup.find('dt', text='Attached Garage')
        attached_garage = attached_garage_dt.find_next_sibling('dd', class_='detail').text.strip() if attached_garage_dt else None

        road_frontage_dt = listing_soup.find('dt', text='Road Frontage')
        road_frontage = road_frontage_dt.find_next_sibling('dd', class_='detail').text.strip() if road_frontage_dt else None

        new_construction_dt = listing_soup.find('dt', text='New Construction')
        new_construction = new_construction_dt.find_next_sibling('dd', class_='detail').text.strip() if new_construction_dt else None

        year_built_dt = listing_soup.find('dt', text='Year Built')
        year_built = year_built_dt.find_next_sibling('dd', class_='detail').text.strip() if year_built_dt else None

        common_interest_dt = listing_soup.find('dt', text='Common Interest')
        common_interest = common_interest_dt.find_next_sibling('dd', class_='detail').text.strip() if common_interest_dt else None

        days_on_market_span = listing_soup.find('span', text='Days on OneHome')
        days_on_market = days_on_market_span.find_next_sibling('span').text.strip() if days_on_market_span else None

        # Extract the desired information from the listing page
        listing_data = {
            'MLS #': listing_soup.find('p', class_='mls').text.strip() if listing_soup.find('p', class_='mls') else None,
            'List Price': list_price,
            'Sell Price': listing_soup.find('p', class_='price').text.strip() if listing_soup.find('p', class_='price') else None,
            'Address': listing_soup.find('p', class_='address-line-one').text.strip() if listing_soup.find('p',
                                                                                                   class_='address-line-one') else None,
            'Structure Type': structure_type,
            'Property Type': property_type,
            'Beds': beds,
            'Full Baths': full_baths,
            'Half Baths': half_baths,
            'Square Footage': square_footage,
            'Lot Size': lot_size,
            'HOA Fee': hoa_fee,
            'Parking Spots': parking_spots,
            'Garage Spaces': garage_spaces,
            'Closed On': closed_on,
            'Stories': stories,
            'Style': style,
            'Attached Garage': attached_garage,
            'Road Frontage': road_frontage,
            'New Construction': new_construction,
            'Year Built': year_built,
            'Common Interest': common_interest,
            'Days On Market': days_on_market,
            # Add more fields as needed
        }

        data.append(listing_data)

    driver.quit()

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Exported data set
    df.to_csv('re_south.csv', index=False)

    return df

extracted_data = webListings()
print(extracted_data)
