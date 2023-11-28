import { FC } from 'react';
import styles from './Loading.module.scss';

interface INameAnim {
	arrAnimation: string[];
}

const Loading: FC<INameAnim> = ({ arrAnimation }) => {
	return (
		<div className={styles.wrapper__loading}>
			{arrAnimation.map(anim => {
				return (
					<div
						key={anim}
						className={styles.test}
						style={{ animation: `${anim} 3s linear infinite` }}
					></div>
				);
			})}

			<svg
				className='svg-animation'
				width='100'
				height='100'
				xmlns='http://www.w3.org/2000/svg'
			>
				<circle
					cx='50'
					cy='50'
					r='40'
					stroke='#3498db'
					strokeWidth='4'
					fill='none'
				>
					<animate
						attributeName='stroke-dashoffset'
						dur='2s'
						from='0'
						to='502'
						repeatCount='indefinite'
					/>
					<animate
						attributeName='stroke-dasharray'
						dur='2s'
						values='150.79644737231007 100.53096491487338;1 250;150.79644737231007 100.53096491487338'
						repeatCount='indefinite'
					/>
				</circle>
			</svg>
		</div>
	);
};

export default Loading;
