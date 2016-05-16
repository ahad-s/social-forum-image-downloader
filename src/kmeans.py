import math
import string

num_comments = 0
word_freq_global = {}
comment_highest_wordcount = (None, 0)

class Comment(object):

	def __init__(self, comment_str):

		global comment_highest_wordcount
		global num_comments

		word_list = self.preprocess_comment(comment_str)
		total_words = len(word_list)

		if total_words > comment_highest_wordcount[1]:
			comment_highest_wordcount = (self, total_words)

		num_comments += 1

		self.term_freq = self.calculate_term_freq(comment_str, word_list, total_words)

		self.inv_doc_freq = self.calculate_inv_doc_freq(comment_str, word_list)

		self.tf_idf = {word: term_freq[word] * inv_doc_freq[word] for word in word_list}


	def get_tf(self):
		return self.term_freq


	def get_idf(self):
		return self.inv_doc_freq


	def get_tf_idf(self):
		return self.tf_idf


	# TODO: Stemming and better NLP instead of .split()
	def preprocess_comment(self, comment):
		comment = comment.translate(None, string.punctuation) # removes punctuation from string, i.e. that's -> thats
		return comment.split()

	def calculate_term_freq(self, comment, word_list, total, total_words):
		global word_freq_global

		tf = {}

		# get initial wordcount in comment
		# note that cloesd form average of all terms is not useful 
		# because we need a second pass anyway for global dict
		for word in word_list:
			if word in tf:
				tf[word] += 1
			else:
				tf[word] = 1


		for word in tf:
			if word in word_freq_global:
				word_freq_global[word] += 1
			else:
				word_freq_global[word] = 1

			tf[word] /= total_words
		return tf


	def calculate_inv_doc_freq(self, comment, word_list):
		return {word: math.log(self.num_comments / word_freq_global[word] for word in word_list}



class KMeansText(object):
	def __init__(self, wordlist):
		self.wordlist = wordlist

		# convert VALUES in each tf-idf idct to a single row with len(words_in_single_comment) columns
		# construct matrix M x N of M comments, and N words/features, let feature = 0 if doesn't exist in row
		# i.e. let N = # of words of comment with highest word count of all comments




	"""
	m = # training examples
	k = set of cluster points, 1 <= k <= m
	c_i = centroids, 1 <= i <= k
	new c_i == mean_i = mean of all points x_i assigned to c_i before
	"""

	def kmeans(self, data, num_clusters):
		centroids = self.random_init(data, num_clusters)

		# TODO: VECTORIZED APPROACH INSTEAD OF ITER

		# for i=1->training_examples:
			# curr_lowest_k = k_1, update curr_lowest_k as you go
			# for k=1 -> total clusters
				# assign lowest k value of ||x_i - mean_k||^2
				# i.e. closest cluster k to the training example

		# for k = 1 -> total clusters
			# calculate mean_k of points assigned to cluster k
			# i.e. mean_1 = 1/4(x_1 + x_4 + x_5 + x_8)
			#      mean_2 = 1/1(x_2), etc.

		pass

	def get_near_centroids(self, data, centroids):
		pass

	def get_means(self, data, c_centroids, k):
		pass

	# K MUST BE LESS THAN NUMBER OF TRAINING EXAMPLES = M!!!
	def random_init(self, data, k):
		# pick random number from 1-k
		# assign cluster_k = x_k, i.e. k random training examples will be centroids
		pass

	def cost_fn(self, data, centroids, means):
		# J = 1/m * norm_2(x_i - mean_(c_i))
		pass

	def perform_kmeans(self, iterations = 50):

		curr_lowest_cost = None

		for i in xrange(iterations):
			# random init
			# kmeans, get centroids and means
			# cost -> add (cost, centroids, means) to list
			pass

		# return lowest cost params in cost_list
		pass

