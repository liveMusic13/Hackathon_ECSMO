import { FC, useEffect, useState } from 'react';
import useActualeDate from '../hooks/useActualDate';
import useRecordQuestion from '../hooks/useRecordQuestion';
import Loading from './loading/Loading';

const App: FC = () => {
	const [isMicro, setIsMicro] = useState<boolean>(true);

	const [animNeznaika, setAnimNeznaika] = useState<string>(
		'i_do_not_know_hello'
	);
	const [durationAudio, setDurationAudio] = useState<number>(0);
	const [textRequest, setTextRequest] = useState<string>('');

	const [isWaitAnswer, setIsWaitAnswer] = useState<boolean>(false);

	const [text, setText] = useState<string>('');
	const [test, setTest] = useState<boolean>(false);
	const [isLoading, setIsLoading] = useState<boolean>(true);

	let nameAudio: string;

	const { actualDate } = useActualeDate();

	const [viewResponce, setViewResponce] = useState<boolean>(false);

	const { startReq, recognition } = useRecordQuestion();

	useEffect(() => {
		let stopAnim = setTimeout(() => {
			setViewResponce(false);
		}, durationAudio);
		return () => {
			clearTimeout(stopAnim);
		};
	}, [durationAudio]);

	let receivedAudioUrl: string;

	const playAudio = (audioUrl: string) => {
		const audio = new Audio(audioUrl);
		audio.play();
		setViewResponce(true);
		setAnimNeznaika('i_do_not_know');
	};

	const getAudioDuration = (audioUrl: string) => {
		return new Promise((resolve, reject) => {
			const audio = new Audio(audioUrl);
			audio.onloadedmetadata = () => {
				const duration = Math.floor(audio.duration * 1000);
				resolve(duration);
			};
			audio.onerror = error => {
				reject(error);
			};
		});
	};

	const receiveAudioStream = async () => {
		const formData = new FormData();
		nameAudio = actualDate();

		formData.append('name', nameAudio);
		formData.append('text', text);

		try {
			const response = await fetch(
				'http://127.0.0.1:8000/questions/',
				{
					method: 'POST',
					body: formData,
				}
			);
			const audioStream: ReadableStream<Uint8Array> | null = response.body;

			const reader: ReadableStreamDefaultReader<Uint8Array> | undefined =
				audioStream?.getReader();
			const audioChunks = [];

			while (true) {
				const { done, value } = await reader!.read();

				if (done) {
					break;
				}

				audioChunks.push(value);
			}

			console.log(audioChunks);
			const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
			const audioUrl = URL.createObjectURL(audioBlob);
			receivedAudioUrl = audioUrl;

			getAudioDuration(audioUrl)
				.then(duration => {
					if (typeof duration === 'number') setDurationAudio(duration);
				})
				.catch(error => {
					console.error('Ошибка при получении длительности аудиофайла:', error);
				});
		} catch (error) {
			console.error('Ошибка при загрузке аудиофайла:', error);
		}
	};

	const addText = async () => {
		try {
			const responce = await fetch(
				`http://127.0.0.1:8000/answers/${nameAudio}/`
			);
			const data = await responce.json();
			const text = data.text;
			setTextRequest(text);
		} catch (error) {
			console.log(error);
		}
	};

	const handleMicroClickPlay = () => {
		if (isMicro) {
			startReq();
			setIsMicro(false);
		}
	};

	useEffect(() => {
		if (!viewResponce) {
			setAnimNeznaika('i_do_not_know_hello');
		} else {
			if (durationAudio <= 6000) {
				let anim = setTimeout(() => {
					setAnimNeznaika('i_do_not_know_wait');
				}, durationAudio - 3000);

				return () => {
					clearTimeout(anim);
				};
			} else {
				let wait = setTimeout(() => {
					setIsWaitAnswer(true);
				}, 3000);

				let anim = setTimeout(() => {
					setIsWaitAnswer(false);
					setAnimNeznaika('i_do_not_know_wait');
				}, durationAudio - 3000);

				return () => {
					clearTimeout(anim);
					clearTimeout(wait);
				};
			}
		}
	}, [viewResponce]);

	recognition.onresult = async function (event: any) {
		const transcript = event.results[0][0].transcript;

		setText(transcript);
		if (event.results[0].isFinal) {
			setIsMicro(true);
		}
		setTest(true);
	};

	useEffect(() => {
		const fetchData = async () => {
			await receiveAudioStream();
			await addText();
			await playAudio(receivedAudioUrl);
		};

		if (test) {
			fetchData();
			setTest(false);
		}
	}, [test]);

	useEffect(() => {
		const animLoading = setTimeout(() => {
			setIsLoading(false);
		}, 13000);

		return () => {
			clearTimeout(animLoading);
		};
	}, []);
	const arrAnimation = [
		'i_do_not_know',
		'i_do_not_know_wait',
		'i_do_not_know_hello',
		'negative_response',
		'micro',
		'bg_main',
	];

	return (
		<>
			{isLoading ? (
				<Loading arrAnimation={arrAnimation} />
			) : (
				<div className='wrapper__app'>
					<img
						src='./images/SkillFactory.svg'
						alt='img'
						className='logo-skillfactory'
					/>
					<img src='./images/ecsmo.jpg' alt='img' className='logo-ecsmo' />
					{!viewResponce ? (
						<img className='app__hello' src='./images/hello.png' alt='hello' />
					) : (
						<p className='text_answer'>{textRequest}</p>
					)}
					{isWaitAnswer ? (
						<div className='animation_wait'></div>
					) : (
						<div
							className='animation'
							style={{ animation: `${animNeznaika} 3s linear infinite` }}
						></div>
					)}

					<div className='block__app__micro'>
						{isMicro ? (
							<img
								className='app__micro'
								src='./images/micro.png'
								alt='micro'
								onClick={handleMicroClickPlay}
							/>
						) : (
							<div className='app__micro_active'></div>
						)}
					</div>
				</div>
			)}
		</>
	);
};

export default App;
