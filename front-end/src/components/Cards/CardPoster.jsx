import React from 'react';
import styles from './CardPoster.module.css';
import { FaStar, FaQuestion } from "react-icons/fa6";

const CardPoster = ({img, title, estrelas}) => {
    return (
        <div className={styles.CardPoster}>
            <img src={img} />
            <h3 className={styles.CardPosterH3}>{title}</h3>
            <div className={styles.CardPosterStars}>
                {estrelas === 0 ? (
                    <FaQuestion key={index} className={styles.starIcon} />
                ) : (
                    Array.from({ length: estrelas }, (_, index) => (
                        <FaStar key={index} className={styles.starIcon} />
                    ))
                )}
            </div>
        </div>
    );
}

export default CardPoster;