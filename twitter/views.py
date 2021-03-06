from django.shortcuts import render
from . import api
from sarprit.architecture import classify
try:
	from html.parser import HTMLParser
except:
	from HTMLParser import HTMLParser
import re

def home(request, restaurant):
	reviews = api.search(restaurant)

	positives = []
	negatives = []
	neutrals = []
	sentences_by_clue = []

	f_sentences = []
	h_sentences = []
	m_sentences = []
	g_sentences = []

	for review in reviews:
		unescape = HTMLParser().unescape

		review.text = unescape(review.text)
		review.user.name = unescape(review.user.name)

		# remove links from tweets
		review.text = re.sub(r'(https?://[A-Za-z0-9]+\.[A-Za-z0-9]+/[A-Za-z0-9]+) *', '', review.text)

		classification = classify(review.text)
		print(classification)

		prediction = classification[0]
		sentences_by_clue.append(classification[1])

		[f_sentences.append(sentence) for sentence in classification[1][0]]
		[h_sentences.append(sentence) for sentence in classification[1][1]]
		[m_sentences.append(sentence) for sentence in classification[1][2]]
		[g_sentences.append(sentence) for sentence in classification[1][3]]

		if prediction > 3:
			positives.append(review)
		elif prediction < 3:
			negatives.append(review)
		else:
			neutrals.append(review)

	return render(request, 'twitter/index.html',
		{
			'positives': positives, 'negatives': negatives,
			'neutrals': neutrals, 'restaurant': restaurant,
			'positives_count': len(positives) * 100 / len(reviews),
			'negatives_count': len(negatives) * 100 / len(reviews),
			'neutrals_count': len(neutrals)* 100 / len(reviews),
			'f_count': len(f_sentences),
			'h_count': len(h_sentences),
			'm_count': len(m_sentences),
			'g_count': len(g_sentences),
			'sentences_by_clue': sentences_by_clue
		})
