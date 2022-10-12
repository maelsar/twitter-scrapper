# Twitter Scraper Webapp
#### Video Demo:  <https://youtu.be/YieM-TiRKZk>
#### Description: 
Scrape Twitter from any user profile on the social platform, and collect data such as tweets, URLs, date and time of tweets, and usernames. Filter your search by typing in a twitter keyword, hashtag, or the username. Run the scraper and download your data in CSV format. Leverage the twitter scraper to get a leg up on whatever is trending, and keep track of user sentiment. It is a useful tool to collect data and take note of emerging trends.

### **Instructions:**

1. Keyword of Keywords Search Field - You can input one or more words. Search will find content containing the the word to be matched.  If more than one word is provided then match return **MUST** contain all the specified words. Hashtags and cashtags (i.e. #BTC $eth) are also valid words.

2. User Search Field - You can search for tweets pertaining from a certain Twitter username or Twitter handle.  @username or username are both allowed (i.e. @elonmusk or elonmusk).

3. Beginning Date Field - This will narrow search from **starting** date.
4. End Date Field - This will narrow search until **ending** date.

   **NOTE :**  It is valid either one or both fields to be filled.  If only **Begining Date** is filled then search will begin search from desired date and end will default to most recent.  If only **End Date** is filled then beginning date will default to earliest tweet in the database and stop searching on the desired End Date.

5. Limit Search Field - is the number of tweets that will be recovered. It is possible to be returned with tweets less than the limit search maximum number if there are not enough tweets that match the desired criteria.  A maximum of 500 tweets was impossed to limit the runtime of the hosting server and conserve resources.  If an input more than 500 is used then it will default to 500.

#### **Any combination of the search is valid**


6. **Return Parameters:**
    - URL - This will return the URL of the Tweet
    - Date - This will return the date and time of the Tweet
    - User Name - This will return the user name of the matching Tweet
    - Content - This will return the content in the tweet (not photos)
    
    If no boxes were ticked then it will default to all boxes ticked.

7. Search - This button will execute the search.

### **Search Results Page**
You will be previewed with the first 5 matches from the search criteria and with the **Return Parameters** specified.
This is to verify to you if it indeed the correct data that you want.

### **Download CSV**
This will initiate a download to a CSV using all the tweets from your search criteria with the limit search.  

**NOTE :**  The CSV is ready to be imported into a database or dataframe and will have column names accordingly.
**Also, when looking at the CSV, it may look like there is no order especially when returning CONTENT.  This is because of "\n" (newline) within the content but I assure you that valid.

### **Remarks**
This was created as a final project for my CS50x course and as a tool to use after i took a Google Data Analytics course.  I inded to use this website to gather raw data from twitter and make sentiment analysis for future projects related to data analytics.

This was created with mainly with tools I learned from CS50x.  The journey long and brain racking but I enjoyed both CS50x and would recommend this course to fellow aspiring developers.

Summary of tools used for this project:
- Frontend Framework: Bulma
- Database: SQLite
- Backend Language: Python
- Backend Framework: Flask
- Hosting: Wayscript
- Source Code: <https://github.com/maelsar/twitter->