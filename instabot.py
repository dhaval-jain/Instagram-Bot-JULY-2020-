
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
#driver = webdriver.Chrome(r"C:/Users/michael/Downloads/chromedriver_win32/chromedriver.exe")
class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(5)

        #self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        #sleep(2)


        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(5)

        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
        .click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(5)

        #self.driver.find_element_by_partial_link_text("following").click()
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/following')]".format(self.username))\
            .click()
        following = self._get_names()
        print(following)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/followers')]".format(self.username))\
            .click()
        followers = self._get_names()
        print(followers)

        not_following_back = [user for user in following if user not in followers]
        print(len(not_following_back))
        print(not_following_back)

    def _get_names(self):
        sleep(2)
        #sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView()' ''', sugs''')
        #sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script('''
                var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                fDialog.scrollTop = fDialog.scrollHeight
                ''',scroll_box)
            #ht = self.driver.execute_script("""
            #    arguments[0].scrollTo(0, arguments[0].scrollHeight); 
            #    return arguments[0].scrollHeight;
            #    """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a').get_attribute('href')
        sleep(10)
        print(links)
        names= links
        #names = [name.get_attribute('href') for name in links ]
        sleep(20)
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

my_bot = InstaBot('USERNAME','PASSWORD') # enter your username and password 
my_bot.get_unfollowers()
