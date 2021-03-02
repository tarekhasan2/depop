


class Merchant:
	def __init__(self, url, merchant_name, username, rating, total_review, total_sold, last_active,
		followers, following, description, instagram, facebook, twitter, linkedin, youtube, merchant_site):

		self.url 				= url
		self.merchant_name		= merchant_name
		self.username 			= username
		self.rating 			= rating
		self.total_review 		= total_review
		self.total_sold 		= total_sold
		self.last_active 		= last_active
		self.followers 			= followers
		self.following 			= following
		self.description 		= description
		self.instagram 			= instagram
		self.facebook 			= facebook
		self.twitter 			= twitter
		self.linkedin 			= linkedin
		self.youtube 			= youtube
		self.merchant_site 		= merchant_site


	def __repr__(self):
		return "Merchant('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
			self.url, self.merchant_name, self.username, self.rating, self.total_review, self.total_sold,
			self.last_active, self.followers, self.following, self.description, self.instagram,
			self.facebook, self.twitter, self.linkedin, self.youtube, self.merchant_site
			)