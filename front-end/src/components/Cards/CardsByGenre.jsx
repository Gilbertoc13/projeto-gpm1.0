import React, { useState, useEffect } from "react";
import styles from './CardsByGenre.module.css';
import CardPoster from "./CardPoster";

function ContainerCards({ title, type }) {
    const API_KEY = '2da54e7773e1f650b5dccea60ca453a7';
    const [content, setContent] = useState(null);
    const [selectedGenre, setSelectedGenre] = useState(null);
    const [genreContent, setGenreContent] = useState([]);

    useEffect(() => {
        fetch(`https://api.themoviedb.org/3/trending/${type}/week?api_key=${API_KEY}&language=pt-BR`)
            .then(response => response.json())
            .then(response => {
                setGenreContent(response.results);
            })
            .catch(err => console.error(err));

        fetch(`https://api.themoviedb.org/3/genre/${type}/list?api_key=${API_KEY}&language=pt-BR`)
            .then(response => response.json())
            .then(response => {
                setContent(response);
            })
            .catch(err => console.error(err));
    }, [type]);

    const handleGenreClick = (genreId, genreName) => {
        if(type === "tv"){
            setSelectedGenre(`Séries ${genreName.toLowerCase()}`);
        } else{
            setSelectedGenre(`Filmes ${genreName.toLowerCase()}`);
        }

        fetch(`https://api.themoviedb.org/3/discover/${type}?api_key=${API_KEY}&language=pt-BR&with_genres=${genreId}&certification_country=BR&certification.lte=14&page=1`)
            .then(response => response.json())
            .then(response => {
                setGenreContent(response.results);
            })
            .catch(err => console.error(err));
    };

    return (
        <div className={styles.ContainerCards}>
            <h2>{selectedGenre ? selectedGenre : title}</h2>
            <div className={styles.divGeneros}>
                {content && content.genres.map(genero => (
                    <div key={genero.id} className={styles.Genero} onClick={() => handleGenreClick(genero.id, genero.name.split(' ')[0])}>
                        {genero.name.split(' ')[0]}
                    </div>
                ))}
            </div>
            <div className={styles.divCards}>
                {genreContent.map(item => (
                    <CardPoster key={item.id}
                        img={`https://image.tmdb.org/t/p/w500/${item.poster_path}`}
                        title={type === "tv" ? item.name : item.title}
                        estrelas={type === "tv" ? (item.vote_average/2).toFixed(1) : (item.vote_average/2).toFixed(1)}
                    ></CardPoster>
                ))}
            </div>
        </div>
    );
}

export default ContainerCards;
