import React from 'react';
import { Link } from 'react-router-dom';
import styles from './CardDaily.module.css';
import { useState, useEffect } from "react";
import { FaStar, FaLanguage, FaRegCalendar } from 'react-icons/fa6';

function CardDaily({ tipo, id, overview, vote_average, original_language, release_date, backdrop_path, title }) {
  const [logo, setLogo] = useState(null);

  useEffect(() => {
    fetch(`https://api.themoviedb.org/3/${tipo}/${id}/images?api_key=${import.meta.env.VITE_TMDB_API}`)
      .then(response => response.json())
      .then(data => {
        const ptItem = data.logos.find(item => item.iso_639_1 === 'pt');
        const selectedItem = ptItem || data.logos.find(item => item.iso_639_1 === 'en');
        setLogo(selectedItem);
      });
  }, [id]);

  return (
    <Link to={`/details/${tipo}/${id}`} className={styles.DailyDiv}>
      <div className={styles.DailyBackdrop} style={{ backgroundImage: `url(${backdrop_path})` }}>
        <div className={styles.DailyFade}>
          {logo ? (
            <>
              <img className={styles.DailyLogo} src={`https://image.tmdb.org/t/p/w200${logo.file_path}`} alt="" />
              <p className={styles.DailyOverview}>{overview}</p>
            </>
          ) : (
            <>
              <h1 className={styles.DailyTitle}>{title}</h1>
              <p className={styles.DailyOverview}>{overview}</p>
            </>
          )}
        </div>
      </div>
      <div className={styles.DailyInfos}>
        <div className={styles.DailyInfo}>
          <FaStar></FaStar>
          <p>{vote_average}</p>
        </div>
        <div className={styles.DailyInfo}>
          <FaLanguage></FaLanguage>
          <p>{original_language}</p>
        </div>
        <div className={styles.DailyInfo}>
          <FaRegCalendar></FaRegCalendar>
          <p>{release_date}</p>
        </div>
      </div>
    </Link>
  );
}

export default CardDaily;
