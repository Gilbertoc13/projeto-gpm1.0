import React from 'react';
import styles from './CardPoster.module.css';

const CardPoster = ({img, title, estrelas}) => {
    return (
        <div className={styles.CardPoster}>
            <img src={img} />
            <h3 className={styles.CardPosterH3}>{title}</h3>
            <h4 className={styles.CardPosterH4}>{estrelas} Estrelas</h4>
        </div>
    );
}

export default CardPoster;