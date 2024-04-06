import { FaStar, FaCalendar } from "react-icons/fa";
import { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import styles from './CardTrend.module.css';

function CardTrend({ id, tipo, isMiddlePage}) {
    const [content, setContent] = useState(null);
    const [logo, setLogo] = useState(null);

    useEffect(() => {
        fetch(`https://api.themoviedb.org/3/${tipo}/${id}?api_key=${import.meta.env.VITE_TMDB_API}&append_to_response=images%2Caggregate_credits%2Cwatch_providers%2Csimilar%2Cexternal_ids%2Ccontent_ratings%2Creleases&language=pt-BR`)
            .then(response => response.json())
            .then(response => {
                setContent(response);
            })
            .catch(err => console.error(err));

        fetch(`https://api.themoviedb.org/3/${tipo}/${id}/images?api_key=${import.meta.env.VITE_TMDB_API}`)
            .then(response => response.json())
            .then(data => {
                const ptItem = data.logos.find(item => item.iso_639_1 === "pt");
                const selectedItem = ptItem || data.logos.find(item => item.iso_639_1 === "en");
                setLogo(selectedItem);
            });
    }, [id]);

    function redirecionar() {
        console.log("Clicou card");
    }

    const backgroundImageStyle = content ? { backgroundImage: `url(https://image.tmdb.org/t/p/original${content.backdrop_path})` } : {};
    let ageRating
    if(tipo === "tv") {
        ageRating = content?.content_ratings?.results.find(item => item.iso_3166_1 === "BR")?.rating || content?.content_ratings?.results.find(item => /^\d+$/.test(item.iso_3166_1))?.rating || '?';
    } else{
        ageRating = content?.releases?.countries.find(item => item.iso_3166_1 === "BR")?.certification || '?';
    }    const destaqueClasses = isMiddlePage ? `${styles.Fade} ${styles.MiddlePage}` : styles.Fade;

    return (
        <Link to={`/details/${tipo}/${id}`} className={styles.Destaque} onClick={redirecionar} style={backgroundImageStyle}>
            <div className={destaqueClasses}>
                <img src={`https://image.tmdb.org/t/p/original${logo?.file_path}`} alt="" />
                <p className={styles.Overview}>{content?.overview}</p>
                <div className={styles.Infos}>
                    <FaStar />
                    <h2 className={styles.InfoH2}>{((content?.vote_average.toFixed(1)/2).toFixed(1))}</h2>
                    <FaCalendar />
                    <h2 className={styles.InfoH2}>{tipo === "tv" ? content?.first_air_date?.split('-')[0] : content?.release_date?.split('-')[0]}</h2>
                </div>
                <div className={styles.Infos}>
                    <div className={styles.ageRestricted}>
                        <h2 className={styles.ageRestrictedText}>{ageRating}</h2>
                    </div>
                    <h2 className={styles.InfoH2}>{content?.genres.map(genre => genre.name).join(", ")}</h2>
                </div>
            </div>
        </Link>
    );
}

export default CardTrend;
