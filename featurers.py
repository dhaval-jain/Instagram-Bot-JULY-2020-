from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager


class InstagramBot():
    def __init__(self, email, password):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)
        emailInput = self.browser.find_element_by_xpath("//input[@name=\"username\"]")
        passwordInput = self.browser.find_element_by_xpath("//input[@name=\"password\"]")

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Follow'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")

    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        try:
            self.browser.find_element_by_xpath('//button[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]').click()
            time.sleep(2)
            self.browser.find_element_by_xpath('//button[@class="aOOlW -Cab_   "]').click()
            time.sleep(2)
            print("unfollowed "+username)
        except:
            print("You dont follow "+username)

        
    def getUserFollowers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')

        ele = self.browser.find_element_by_css_selector("ul li a span")
        max = int(ele.get_attribute('title'))

        followersLink.click()
        time.sleep(4)
        followersList = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        followersList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)
            followersList.click()
        
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')[26:-1]

            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers
    

    def getUserFollowing(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)

        ele = self.browser.find_element_by_css_selector("ul li:nth-child(3) a span").text#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > span
        max = int(ele)

        followingLink = self.browser.find_element_by_xpath("//a[contains(@href,'/{}/following')]".format(self.email))
        followingLink.click()
        time.sleep(4)
        followingList = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))
        followingList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowingInList < max-1):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))
            print(numberOfFollowingInList)
            followingList.click()
        
        following = []
        for user in followingList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')[26:-1]
            print(userLink)
            following.append(userLink)
            if (len(following) == max):
                break
        return following

bot = InstagramBot('USERNAME', 'PASSWORD')
bot.signIn()
time.sleep(3)
#bot.followWithUsername('therock')
#bot.unfollowWithUsername('therock')
#followers = bot.getUserFollowers('_jaindhaval_', None)
following = bot.getUserFollowing('_jaindhaval_',None)

#not_following_back = [users for users in following if users not in  followers]
#print(len(not_following_back))
#print(not_following_back)
