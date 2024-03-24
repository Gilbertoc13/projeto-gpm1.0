import { useEffect, useState } from 'react';
import styles from './DailyGrid.module.css';
import CardDaily from '../Cards/CardDaily';

function DailyGrid({tipo}) {
    const [trends, setTrends] = useState([]);

    useEffect(() => {
        fetch(`https://api.themoviedb.org/3/trending/${tipo}/day?api_key=${import.meta.env.VITE_TMDB_API}&language=pt-BR`)
            .then(response => response.json())
            .then(data => setTrends(data.results.slice(1, 4)));
    }, []);

    return (
        <div className={styles.DailyGrid}>
            {trends.map(trend => (
                <CardDaily
                    key={trend.id}
                    tipo={trend.media_type}
                    id={trend.id}
                    overview={trend.overview}
                    vote_average={(trend.vote_average.toFixed(1)/2).toFixed(1)}
                    original_language={trend.original_language.toUpperCase()}
                    release_date={tipo === 'tv' ? trend.first_air_date.split('-')[0] : trend.release_date.split('-')[0]}
                    backdrop_path={`https://image.tmdb.org/t/p/original/${trend.backdrop_path}`}
                    title={trend.title || trend.name}
                />
            ))}
        </div>
    );
}

export default DailyGrid;