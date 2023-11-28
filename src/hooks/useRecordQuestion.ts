const useRecordQuestion = () => {
	// @ts-ignore
	const recognition: any = new (window.SpeechRecognition ||
		// @ts-ignore
		window.webkitSpeechRecognition)();

	recognition.lang = 'ru-RU';

	const startReq = () => {
		recognition.start();
	};

	return { startReq, recognition };
};

export default useRecordQuestion;
