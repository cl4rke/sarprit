from survey.models import Review, Sentence
from sarprit.shortcuts import normalize_sentiment

def get_subjectivity_classifier_accuracy(sentences, with_additional_data):
	print("Accuracy of Subjectivity Classifier:")
	from .examples import classifier1

	ts = []
	to = []
	fs = []
	fo = []

	s = []
	o = []

	for sentence in sentences:
		subjective = classifier1.predict([sentence.sentence])[0]
		if sentence.subjective:
			s.append(sentence)
			if subjective == 0:
				ts.append(sentence)
			else:
				fo.append(sentence)
		else:
			o.append(sentence)
			if subjective == 0:
				fs.append(sentence)
			else:
				to.append(sentence)

	print(len(ts), len(fs), len(to), len(fo))

	ps = len(ts)/(len(ts)+len(fs) or 1)
	po = len(to)/(len(to)+len(fo) or 1)

	rs = len(ts)/(len(s) or 1)
	ro = len(to)/(len(o) or 1)

	f1s = 2 * ((ps * rs)/(ps + rs or 1))
	f1o = 2 * ((po * ro)/(po + ro or 1))

	print("Subjective:")
	print("\tPrecision:", ps)
	print("\tRecall:   ", rs)
	print("\tF1-score: ", f1s)
	print()

	print("Objective:")
	print("\tPrecision:", po)
	print("\tRecall:   ", ro)
	print("\tF1-score: ", f1o)
	print()

	if with_additional_data:
		print("Additional Data:")
		print("\tFalse Subjective:", '\n\t\t'.join([sentence.__str__() for sentence in fs]))
		print("\tFalse Objective:", '\n\t\t'.join([sentence.__str__() for sentence in fo]))
		print()

def get_clues_classifier_accuracy(sentences, with_additional_data):
	print("Accuracy of Clues Classifier:")
	from .examples import classifier2

	tf = []
	th = []
	tm = []
	tg = []

	ff = []
	fh = []
	fm = []
	fg = []

	f = []
	h = []
	m = []
	g = []

	for sentence in sentences:
		clue1 = sentence.clue
		clue2 = classifier2.predict([sentence.sentence])[0]

		if clue1:
			if clue1 is 'f': # functional
				f.append(sentence)
				if clue2 == 0:
					tf.append(sentence)
				elif clue2 == 1:
					fh.append(sentence)
				elif clue2 == 2:
					fm.append(sentence)
				elif clue2 == 3:
					fg.append(sentence)
			elif clue1 is 'h': # humanic
				h.append(sentence)
				if clue2 == 0:
					ff.append(sentence)
				elif clue2 == 1:
					th.append(sentence)
				elif clue2 == 2:
					fm.append(sentence)
				elif clue2 == 3:
					fg.append(sentence)
			elif clue1 is 'm': # mechanic
				m.append(sentence)
				if clue2 == 0:
					ff.append(sentence)
				elif clue2 == 1:
					fh.append(sentence)
				elif clue2 == 2:
					tm.append(sentence)
				elif clue2 == 3:
					fg.append(sentence)
			elif clue1 is 'g': # general
				g.append(sentence)
				if clue2 == 0:
					ff.append(sentence)
				elif clue2 == 1:
					fh.append(sentence)
				elif clue2 == 2:
					fm.append(sentence)
				elif clue2 == 3:
					tg.append(sentence)

	print(len(tf), len(ff), len(th), len(fh), len(tm), len(fm), len(tg), len(fg))

	pf = len(tf)/(len(tf)+len(ff) or 1)
	ph = len(th)/(len(th)+len(fh) or 1)
	pm = len(tm)/(len(tm)+len(fm) or 1)
	pg = len(tg)/(len(tg)+len(fg) or 1)

	rf = len(tf)/(len(f) or 1)
	rh = len(th)/(len(h) or 1)
	rm = len(tm)/(len(m) or 1)
	rg = len(tg)/(len(g) or 1)

	f1f = 2 * ((pf * rf)/(pf + rf or 1))
	f1h = 2 * ((ph * rh)/(ph + rh or 1))
	f1m = 2 * ((pm * rm)/(pm + rm or 1))
	f1g = 2 * ((pg * rg)/(pg + rg or 1))

	print("Functional:")
	print("\tPrecision:", pf)
	print("\tRecall:   ", rf)
	print("\tF1-score: ", f1f)
	print()

	print("Humanic:")
	print("\tPrecision:", ph)
	print("\tRecall:   ", rh)
	print("\tF1-score: ", f1h)
	print()

	print("Mechanic:")
	print("\tPrecision:", pm)
	print("\tRecall:   ", rm)
	print("\tF1-score: ", f1m)
	print()

	print("General:")
	print("\tPrecision:", pg)
	print("\tRecall:   ", rg)
	print("\tF1-score: ", f1g)
	print()

	if with_additional_data:
		print("Additional Data:")
		print("\tFalse Functional:", '\n\t\t'.join([sentence.__str__() for sentence in ff]))
		print("\tFalse Humanic:", '\n\t\t'.join([sentence.__str__() for sentence in fh]))
		print("\tFalse Mechanic:", '\n\t\t'.join([sentence.__str__() for sentence in fm]))
		print("\tFalse General:", '\n\t\t'.join([sentence.__str__() for sentence in fg]))
		print()

def get_clues_sentiment_classifier_accuracy(sentences, with_additional_data):
	print("Accuracy of Clues Sentiment Classifier:")

	clues = ['f', 'h', 'm', 'g']
	full_clue_words = ['Functional', 'Humanic', 'Mechanic', 'General']

	for i in range(4):
		print("Accuracy of %s Sentiment Classifier:"%full_clue_words[i])
		clue = clues[i]

		tp = []
		te = []
		tn = []

		fp = []
		fe = []
		fn = []

		p = []
		e = []
		n = []

		for sentence in [sentence for sentence in sentences if sentence.clue == clue]:
			if clue == 'f':
				from .examples import classifier3a
				classifier = classifier3a
			elif clue == 'h':
				from .examples import classifier3b
				classifier = classifier3b
			elif clue == 'm':
				from .examples import classifier3c
				classifier = classifier3c
			elif clue == 'g':
				from .examples import classifier3d
				classifier = classifier3d

			sentiment1 = normalize_sentiment(sentence.rating)
			sentiment2 = normalize_sentiment(int(classifier.predict([sentence.sentence])[0]))

			if sentiment1 == 0: # negative
				n.append(sentence)
				if sentiment2 == 0: # negative
					tn.append(sentence)
				elif sentiment2 == 1: # neutral
					fe.append(sentence)
				elif sentiment2 == 2: # positive
					fp.append(sentence)
			elif sentiment1 == 1: # neutral
				e.append(sentence)
				if sentiment2 == 0: # negative
					fn.append(sentence)
				elif sentiment2 == 1: # neutral
					te.append(sentence)
				elif sentiment2 == 2: # positive
					fp.append(sentence)
			elif sentiment1 == 2: # positive
				p.append(sentence)
				if sentiment2 == 0: # negative
					fn.append(sentence)
				elif sentiment2 == 1: # neutral
					fe.append(sentence)
				elif sentiment2 == 2: # positive
					tp.append(sentence)

		print(len(tp), len(fp), len(te), len(fe), len(tn), len(fn))

		pp = len(tp)/(len(tp)+len(fp) or 1)
		pe = len(te)/(len(te)+len(fe) or 1)
		pn = len(tn)/(len(tn)+len(fn) or 1)

		rp = len(tp)/(len(p) or 1)
		re = len(te)/(len(e) or 1)
		rn = len(tn)/(len(n) or 1)

		f1p = 2 * ((pp * rp)/(pp + rp or 1))
		f1e = 2 * ((pe * re)/(pe + re or 1))
		f1n = 2 * ((pn * rn)/(pn + rn or 1))

		print("Positive:")
		print("\tPrecision:", pp)
		print("\tRecall:   ", rp)
		print("\tF1-score: ", f1p)
		print()

		print("Neutral:")
		print("\tPrecision:", pe)
		print("\tRecall:   ", re)
		print("\tF1-score: ", f1e)
		print()

		print("Negative:")
		print("\tPrecision:", pn)
		print("\tRecall:   ", rn)
		print("\tF1-score: ", f1n)
		print()

		if with_additional_data:
			print("Additional Data:")
			print("\tFalse Positive:", '\n\t\t'.join([sentence.__str__() for sentence in fp]))
			print("\tFalse Neutral:", '\n\t\t'.join([sentence.__str__() for sentence in fe]))
			print("\tFalse Negative:", '\n\t\t'.join([sentence.__str__() for sentence in fn]))
			print()

def get_overall_sentiment_classifier_accuracy(reviews, without_clues, with_additional_data):
	print(
		"Accuracy of Overall Sentiment Classifier",
		"(clueless):" if without_clues else "(with clues):"
		)

	tp = []
	te = []
	tn = []

	fp = []
	fe = []
	fn = []

	p = []
	e = []
	n = []

	clues = ['Functional', 'Humanic', 'Mechanic', 'General']

	for review in reviews:
		if without_clues:
			from .architecture import classify_without_clues
			sentiment, sentences = classify_without_clues(review.raw_string())
		else:
			from .architecture import classify
			sentiment, sentences = classify(review.raw_string())

		sentiment1 = normalize_sentiment(review.overall_sentiment)
		sentiment2 = normalize_sentiment(sentiment)

		if sentiment1 == 0: # negative
			n.append(
				review.__str__()+'\n\t\t\t'+
				('\n\t\t\t'.join([
					clues[i]+": "+'\n\t\t\t\t'.join([
						sentence for sentence in sentences[i]
					]) for i in range(4)
				]) if not without_clues else '')
			)
			if sentiment2 == 0: # negative
				tn.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
			elif sentiment2 == 1: # neutral
				fe.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
			elif sentiment2 == 2: # positive
				fp.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
		elif sentiment1 == 1: # neutral
			e.append(
				review.__str__()+'\n\t\t\t'+
				('\n\t\t\t'.join([
					clues[i]+": "+'\n\t\t\t\t'.join([
						sentence for sentence in sentences[i]
					]) for i in range(4)
				]) if not without_clues else '')
			)
			if sentiment2 == 0: # negative
				fn.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
			elif sentiment2 == 1: # neutral
				te.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
			elif sentiment2 == 2: # positive
				fp.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
		elif sentiment1 == 2: # positive
			p.append(
				review.__str__()+'\n\t\t\t'+
				('\n\t\t\t'.join([
					clues[i]+": "+'\n\t\t\t\t'.join([
						sentence for sentence in sentences[i]
					]) for i in range(4)
				]) if not without_clues else '')
			)
			if sentiment2 == 0: # negative
				fn.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
			elif sentiment2 == 1: # neutral
				fe.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)
			elif sentiment2 == 2: # positive
				tp.append(
					review.__str__()+'\n\t\t\t'+
					('\n\t\t\t'.join([
						clues[i]+": "+'\n\t\t\t\t'.join([
							sentence for sentence in sentences[i]
						]) for i in range(4)
					]) if not without_clues else '')
				)

	print(len(tp), len(fp), len(te), len(fe), len(tn), len(fn))

	pp = len(tp)/(len(tp)+len(fp) or 1)
	pe = len(te)/(len(te)+len(fe) or 1)
	pn = len(tn)/(len(tn)+len(fn) or 1)

	rp = len(tp)/(len(p) or 1)
	re = len(te)/(len(e) or 1)
	rn = len(tn)/(len(n) or 1)

	f1p = 2 * ((pp * rp)/(pp + rp or 1))
	f1e = 2 * ((pe * re)/(pe + re or 1))
	f1n = 2 * ((pn * rn)/(pn + rn or 1))

	print("Positive:")
	print("\tPrecision:", pp)
	print("\tRecall:   ", rp)
	print("\tF1-score: ", f1p)
	print()

	print("Neutral:")
	print("\tPrecision:", pe)
	print("\tRecall:   ", re)
	print("\tF1-score: ", f1e)
	print()

	print("Negative:")
	print("\tPrecision:", pn)
	print("\tRecall:   ", rn)
	print("\tF1-score: ", f1n)
	print()

	if with_additional_data:
		print("Additional Data:")
		print("\tFalse Positive:", '\n\t\t'.join([review.__str__() for review in fp]))
		print("\tFalse Neutral:", '\n\t\t'.join([review.__str__() for review in fe]))
		print("\tFalse Negative:", '\n\t\t'.join([review.__str__() for review in fn]))
		print()

def get_accuracies(with_additional_data=True):
	print("Initialzing...")
	import sarprit.examples

	print()

	reviews = Review.objects.filter(flag=2)
	sentences = [sentence for review in reviews for sentence in review.sentence_set.all()]


	get_subjectivity_classifier_accuracy(sentences, with_additional_data)
	get_clues_classifier_accuracy(sentences, with_additional_data)
	get_clues_sentiment_classifier_accuracy(sentences, with_additional_data)
	get_overall_sentiment_classifier_accuracy(reviews, True, with_additional_data)
	get_overall_sentiment_classifier_accuracy(reviews, False, with_additional_data)

def get_score(sentences):
	count = len(sentences) or 1
	return sum([sentence.rating for sentence in sentences])/count

def get_clues_impact(f, h, m, g, fscore, hscore, mscore, gscore, sscore):
	fdiff = abs(sscore - fscore) if f is 1 else 0
	hdiff = abs(sscore - hscore) if h is 1 else 0
	mdiff = abs(sscore - mscore) if m is 1 else 0
	gdiff = abs(sscore - gscore) if g is 1 else 0
	diff_sum = (fdiff + hdiff + mdiff + gdiff) or 1

	clues_count = f + h + m + g

	if clues_count > 0:
		fimpact = 1 - fdiff/diff_sum
		himpact = 1 - hdiff/diff_sum
		mimpact = 1 - mdiff/diff_sum
		gimpact = 1 - gdiff/diff_sum
	else:
		fimpact = 0
		himpact = 0
		mimpact = 0
		gimpact = 0

	print(
		"Impact:     %8s    %8s    %8s    %8s  = %8s" % (
		 	"x %2.2f"%(fimpact/((clues_count-1) or 1) if f is 1 else 0),
		 	"x %2.2f"%(himpact/((clues_count-1) or 1) if h is 1 else 0),
		 	"x %2.2f"%(mimpact/((clues_count-1) or 1) if m is 1 else 0),
		 	"x %2.2f"%(gimpact/((clues_count-1) or 1) if g is 1 else 0),
		 	"x 1.00"
		 )
	)

def get_data_ratio():
	reviews = Review.objects.filter(flag=1)
	sentences = [sentence for review in reviews for sentence in review.sentence_set.all()]

	subjective_sentences = [sentence for sentence in sentences if sentence.subjective is True]
	objective_sentences = [sentence for sentence in sentences if sentence.subjective is False]

	print()
	print("Subjective count:", len(subjective_sentences))
	print("Objective count: ", len(objective_sentences))

	f_sentences = [sentence for sentence in sentences if sentence.clue is 'f']
	h_sentences = [sentence for sentence in sentences if sentence.clue is 'h']
	m_sentences = [sentence for sentence in sentences if sentence.clue is 'm']
	g_sentences = [sentence for sentence in sentences if sentence.clue is 'g']

	fp = [sentence for sentence in f_sentences if sentence.rating >  3]
	fe = [sentence for sentence in f_sentences if sentence.rating is 3]
	fn = [sentence for sentence in f_sentences if sentence.rating <  3]

	hp = [sentence for sentence in h_sentences if sentence.rating >  3]
	he = [sentence for sentence in h_sentences if sentence.rating is 3]
	hn = [sentence for sentence in h_sentences if sentence.rating <  3]

	mp = [sentence for sentence in m_sentences if sentence.rating >  3]
	me = [sentence for sentence in m_sentences if sentence.rating is 3]
	mn = [sentence for sentence in m_sentences if sentence.rating <  3]

	gp = [sentence for sentence in g_sentences if sentence.rating >  3]
	ge = [sentence for sentence in g_sentences if sentence.rating is 3]
	gn = [sentence for sentence in g_sentences if sentence.rating <  3]

	print()
	print("F count: %4s | %4s %4s %4s" % (len(f_sentences), len(fp), len(fe), len(fn)))
	print("H count: %4s | %4s %4s %4s" % (len(h_sentences), len(hp), len(he), len(hn)))
	print("M count: %4s | %4s %4s %4s" % (len(m_sentences), len(mp), len(me), len(mn)))
	print("G count: %4s | %4s %4s %4s" % (len(g_sentences), len(gp), len(ge), len(gn)))

	sorted_reviews = [[[[[], []],[[], []]],[[[], []],[[], []]]],[[[[], []],[[], []]],[[[], []],[[], []]]]]

	for review in reviews:
		f=1 if review.sentence_set.filter(clue='f').count() > 0 else 0
		h=1 if review.sentence_set.filter(clue='h').count() > 0 else 0
		m=1 if review.sentence_set.filter(clue='m').count() > 0 else 0
		g=1 if review.sentence_set.filter(clue='g').count() > 0 else 0

		sorted_reviews[f][h][m][g].append(review)

	for g in range(2):
		for m in range(2):
			for h in range(2):
				for f in range(2):
					reviews = sorted_reviews[f][h][m][g]

					reviews_count = len(reviews)

					positive_reviews = [
						review for review in reviews
						if normalize_sentiment(review.overall_sentiment) == 2
					]
					neutral_reviews = [
						review for review in reviews
						if normalize_sentiment(review.overall_sentiment) == 1
					]
					negative_reviews = [
						review for review in reviews
						if normalize_sentiment(review.overall_sentiment) == 0
					]

					fscores = []
					hscores = []
					mscores = []
					gscores = []
					sscores = []

					for review in reviews:
						f_sentences = [
							sentence for sentence in review.sentence_set.all() if sentence.clue is 'f'
						]
						h_sentences = [
							sentence for sentence in review.sentence_set.all() if sentence.clue is 'h'
						]
						m_sentences = [
							sentence for sentence in review.sentence_set.all() if sentence.clue is 'm'
						]
						g_sentences = [
							sentence for sentence in review.sentence_set.all() if sentence.clue is 'g'
						]

						fscore = get_score(f_sentences)
						hscore = get_score(h_sentences)
						mscore = get_score(m_sentences)
						gscore = get_score(g_sentences)

						sscore = review.overall_sentiment

						fscores.append(fscore)
						hscores.append(hscore)
						mscores.append(mscore)
						gscores.append(gscore)
						sscores.append(sscore)

					fscore = sum([score for score in fscores])/(reviews_count or 1)
					hscore = sum([score for score in hscores])/(reviews_count or 1)
					mscore = sum([score for score in mscores])/(reviews_count or 1)
					gscore = sum([score for score in gscores])/(reviews_count or 1)
					sscore = sum([score for score in sscores])/(reviews_count or 1)

					print()
					print("%s%s%s%s: %d | %d %d %d"%(
						"F" if f is 1 else "",
						"H" if h is 1 else "",
						"M" if m is 1 else "",
						"G" if g is 1 else "",
						reviews_count,
						len(positive_reviews),
						len(neutral_reviews),
						len(negative_reviews),
						))
					print(
						"Original:   %8sf + %8sh + %8sm + %8sg = %8s" % (
						 	"%6.2f"%(fscore),
						 	"%6.2f"%(hscore),
						 	"%6.2f"%(mscore),
						 	"%6.2f"%(gscore),
						 	"%6.2f"%(sscore)
						 )
					)
					print(
						"Simplified: %8sf + %8sh + %8sm + %8sg = %8s" % (
						 	"%2.2f"%(fscore/(sscore or 1)),
						 	"%2.2f"%(hscore/(sscore or 1)),
						 	"%2.2f"%(mscore/(sscore or 1)),
						 	"%2.2f"%(gscore/(sscore or 1)),
						 	"%2.2f"%(sscore/(sscore or 1))
						 )
					)
					get_clues_impact(f, h, m, g, fscore, hscore, mscore, gscore, sscore)

def set_review_flags_to_fixed():
	from random import shuffle

	reviews = list(Review.objects.all().exclude(flag=0))

	print("Selecting train and test data...")
	length = len(reviews)
	train_reviews = reviews[:int(length/2)]
	test_reviews  = reviews[int(length/2):]

	print("Train Reviews count:", len(train_reviews))
	print("Test Reviews count: ", len(test_reviews))

	train_ids = [review.id for review in train_reviews]
	test_ids = [review.id for review in test_reviews]

	Review.objects.filter(id__in=train_ids).update(flag=1)
	Review.objects.filter(id__in=test_ids).update(flag=2)

def randomize_review_flags():
	from random import shuffle

	reviews = list(Review.objects.all().exclude(flag=0))

	print("Shuffling reviews...")
	shuffle(reviews)

	print("Selecting train and test data...")
	length = len(reviews)
	train_reviews = reviews[:int(length*3/4)]
	test_reviews  = reviews[int(length*3/4):]

	print("Train Reviews count:", len(train_reviews))
	print("Test Reviews count: ", len(test_reviews))

	train_ids = [review.id for review in train_reviews]
	test_ids = [review.id for review in test_reviews]

	Review.objects.filter(id__in=train_ids).update(flag=1)
	Review.objects.filter(id__in=test_ids).update(flag=2)

def set_review_flags_to_training():
	Review.objects.all().exclude(flag=0).update(flag=1)
