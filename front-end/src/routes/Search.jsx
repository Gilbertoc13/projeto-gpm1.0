import '../index.css';
import { useEffect, useState } from 'react';
import styles from './Search.module.css';
import { Link } from 'react-router-dom';
import { FaSearch } from 'react-icons/fa';
import { FaFaceSadTear } from "react-icons/fa6";
import CardDaily from '../components/Cards/CardDaily';

function Search(){
    const [trends, setTrends] = useState([]);
    const [searchValue, setSearchValue] = useState('');

    useEffect(() => {
        fetch(`https://api.themoviedb.org/3/trending/tv/day?api_key=${import.meta.env.VITE_TMDB_API}&language=pt-BR`)
            .then(response => response.json())
            .then(data => setTrends(data.results));
    }, []);

    const handleSearch = () => {
        fetch(`https://api.themoviedb.org/3/search/multi?api_key=${import.meta.env.VITE_TMDB_API}&language=pt-BR&query=${searchValue}`)
            .then(response => response.json())
            .then(data => {
                setTrends(data.results);
            });
    };

    const handleInputChange = (event) => {
        setSearchValue(event.target.value);
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSearch();
        }
    };

    return(
        <div className={styles.SearchDiv}>
            <div className={styles.DivInput}>
                <input
                    className={styles.InputSearch}
                    type="text"
                    placeholder="Buscar filmes, séries, animes..."
                    value={searchValue}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                />
                <FaSearch onClick={handleSearch} />
            </div>
            <div className={styles.NoResults} style={{ display: trends.length === 0 ? 'flex' : 'none' }}>
                <FaFaceSadTear />
                <p>Nenhum resultado.</p>
            </div>
            {trends.some(trend => trend.media_type === 'person' && trend.profile_path !== null) && (
                <div className={styles.Pessoas}>
                    <h4>Pessoas</h4>
                    <div className={styles.DivPessoas}>
                        {trends
                            .filter(trend => trend.media_type === 'person' && trend.profile_path !== null)
                            .map(trend => (
                                <Link to={`/person/${trend.id}`} key={trend.id} className={styles.DivPessoa}>
                                    <img src={`https://image.tmdb.org/t/p/w100_and_h100_face/${trend.profile_path}`} />
                                    <h1>{trend.name}</h1>
                                </Link>
                            ))}
                    </div>
                </div>
            )}
            <div className={styles.DivResults} style={{ display: trends.length === 0 ? 'none' : 'grid' }}>
                {trends
                    .filter(trend => (trend.media_type === 'tv' || trend.media_type === 'movie') && trend.popularity > 1 && trend.backdrop_path !== null)
                    .map(trend => (
                        <CardDaily
                            key={trend.id}
                            tipo={trend.media_type}
                            id={trend.id}
                            overview={trend.overview ? trend.overview : ''}
                            vote_average={trend.vote_average ? (trend.vote_average.toFixed(1)/2).toFixed(1) : "?"}
                            original_language={trend.original_language ? trend.original_language.toUpperCase() : "?"}
                            release_date={trend.media_type === 'movie' ? trend.release_date?.split('-')[0] : trend.first_air_date?.split('-')[0]}
                            backdrop_path={trend.backdrop_path ? `https://image.tmdb.org/t/p/w500/${trend.backdrop_path}` : 'https://via.placeholder.com/500x281'}
                            title={trend.title || trend.name}
                        />
                    ))}
            </div>
        </div>
    )
}

export default Search;