import React from 'react';
import { Link } from 'react-router-dom';
import styles from './CardPoster.module.css';
import { FaStar, FaQuestion } from "react-icons/fa6";
import { useState, useEffect } from "react";

const CardPoster = ({img, title, estrelas, tipo, id}) => {
    return (
        <Link to={`/details/${tipo}/${id}`} className={styles.CardPoster}>
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
        </Link>
    );
}

export default CardPoster;