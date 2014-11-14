from sarprit import classifiers

def subjective_sentences():
	return [
		"Ang sarap ng pagkain!",
		"Nakakatuwa sila magserve ng pagkain.",
		"Hindi ako naiintindihan ng cashier.",
		"Ang sarap-sarap ng sisig nila at mura pa, paborito na ito ng tropa ko!"
		"#panaloSiKuyangWaiter",
		"Sobrang baho sa lugar nila!",
	]

def objective_sentences():
	return [
		"Ang spaghetti ay isang pagkaing puro pasta.",
		"You are what you eat.",
		"Ang mga kinakain mo ay ang kung sino ikaw",
		"Kumakain kami ngayon sa McDo.",
		"Here at SM Sta Mesa Food Court!",
		"Gagala ba tayo ngayon?",
	]

def subjectivity_classifier():
	ss = subjective_sentences()
	os = objective_sentences()

	training_data = ss + os
	target = [0] * len(ss) + [1] * len(os)

	return classifiers.SubjectivityClassifier().fit(training_data, target)