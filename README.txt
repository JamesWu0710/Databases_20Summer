#######################################################################
This is the list of files in this project
#######################################################################
** We need to create a database named 'ticket' in the local server, then import table_creation.sql to create tables**

DB_Project.py -- Main python code to start the server & execute query & process database etc.
templates:
    custFinalPurchaseSuccessPage.html (Showing messages for successful ticket payment)
	custHomepage.html (customer Homepage after logged in)
	custnotbuy.html  (fail to buy ticket)
	customererror.html (fail to rate and comment)
	customerNotAuthorized.html (customer logged in but visit sites for staff only)
	customersignin.html (customer's log in page)
	customersignup.html (customer's register page)
	custPublicSearch.html (customer search flights)
	custPurchaseDetail.html (customer purchase detail)
	custPurchaseMiddle.html (customer purchase process middle-ground for customer's confirmation)
	custPurchasepage.html (customer purchase page)
	custPurchaseSuccessPage.html (success page after purchasing a ticket)
	custRateComment.html (customer's rate and comment page)
	custSearchFlight.html (customer search flight page)
	custTrackSpending.html (customer track spending page)
	custViewFlight.html (customer view flight page)
	goodbye.html (the page after logged out, will redirect to homepage)
	index.html (homepage)
	loginError.html (showing error messages for non-authorized visits)
	publicsearch.html (public search page)
	Purchasenotgood.html (fail to purchase)
	staffChangeStatus.html (staff change flight status)
	staffCreateAirplane.html (staff add airplane)
	staffCreateAirport.html (staff add airport)
	staffCreateFlight.html (staff add flight)
	staffHomepage.html (staff homepage after logged in)
	staffnotadd.html (fail to create flight)
	staffnotaddairport.html (fail to create airport)
	staffnotaddplane.html (fail to create airplane)
	staffNotAuthorized.html (staff logged in but visit sites for customers only)
	staffnotchange.html (fail to change flight status)
	staffnotfound.html (fail to find available plane)
	staffPublicSearch.html (staff public search page)
	staffsignin.html (staff login page)
	staffsignup.html (staff register page)
	staffsuccess.html (success adding/changing)
	staffViewComments.html (view comment of flights)
	staffViewCustomer.html (view customer of specfic flight/ most frequent customer)
	staffViewFlight.html (staff view flight page)
	staffViewRating.html (staff view rating page)
	staffViewReport.html (staff view report page)
	staffViewReportSpecific.html (staff view report within a specific time range page)
	staffViewSpecific.html (staff view specific customer info page)
	thanksforfeedback.html (will appear after rating and commenting)

static:
	1.png (footer ins picture)
	2.png (footer ins picture)
	3.png (footer ins picture)
	4.png (footer ins picture)
	5.png (footer ins picture)
	6.png (footer ins picture)

	img:
		logo.png
		footer_logo.png
		banner:
			bradcam.png (background picture for customer homepage)
			bradcam2.png (background picture for staff homepage)
			bradcam3.png (background picture for track spending page)
			bradcam4.png (background picture for rate and comment page)
			chicago.png (picture for index page)
			newyork.png (picture for index page)
			sanf.png (picture for index page)
			shanghai.png (picture for index page)
		destination:
			1.png (popular destination picture)
			2.png (popular destination picture)
			3.png (popular destination picture)
			4.png (popular destination picture)
			5.png (popular destination picture)
			6.png (popular destination picture)
		instagram:
			1.png (ins picture)
			2.png (ins picture)
			3.png (ins picture)
			4.png (ins picture)
			5.png (ins picture)
			6.png (ins picture)

	images:
		signin-image.png (logo for signin page)
		signup-image.png (logo for signup page)
		
	css, fonts, js, scss:
		online open templates
		with many revisions and additional features in style.css

table_creation.sql: file to generate required tables in the database.



###############################################################
	
Authors: 
Chengxun(James) Wu       cw2961
Xinyu(Sheron) Gu         xg764
Yinyihong(Emily) Liu     yl5662

Project Orientation:

-Xinyu(Sheron): designing and beautifying websites by writing html and css; writing the summary for all the files in our application with brief description of the functions of different files.
-Chengxun(James): writing Python Flask to build the bridge between html and databases; debugging for the whole project.
-Yinyihong(Emily): writing queries for all the use cases with brief explanation; revising databases and html.

