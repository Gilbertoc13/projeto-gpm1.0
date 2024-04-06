import { useEffect, useState } from 'react';
import '../index.css';
import CardTrend from '../components/Cards/CardTrend';
import CardsByGenre from '../components/Grids/CardsByGenre';
import Ticket from '../components/Ticket';
import Separador from '../components/Separador';
import DailyGrid from '../components/Grids/DailyGrid';

function Home() {
  const [movies, setMovies] = useState([]);
  const [trendingSeries, setTrendingSeries] = useState(null);
  const [trendingMovie, setTrendingMovie] = useState(null);

  useEffect(() => {
    fetch(`https://api.themoviedb.org/3/trending/tv/week?api_key=${import.meta.env.VITE_TMDB_API}&language=pt-BR`)
    .then(response => response.json())
    .then(data => {
      setTrendingSeries(data.results[0]);
    })
    .catch(error => {
      console.error('Error:', error);
    });

    fetch(`https://api.themoviedb.org/3/trending/movie/week?api_key=${import.meta.env.VITE_TMDB_API}&language=pt-BR`)
    .then(response => response.json())
    .then(data => {
      setTrendingMovie(data.results[0]);
    })
    .catch(error => {
      console.error('Error:', error);
    });

    fetch(`https://api.themoviedb.org/3/movie/now_playing?api_key=${import.meta.env.VITE_TMDB_API}&language=pt-BR&region=BR`)
      .then(response => response.json())
      .then(data => {
        setMovies(data.results.slice(0, 6));
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);

  return (
    <div className="App">
      {trendingSeries && (
        <CardTrend id={trendingSeries.id} tipo="tv" isMiddlePage={false}/>
      )}
      <Separador nome="Séries populares hoje" />
      <DailyGrid tipo='tv'/>
      <CardsByGenre title={"Séries da semana"} type={"tv"} />

      {trendingMovie && (
        <CardTrend id={trendingMovie.id} tipo="movie" isMiddlePage={true}/>
      )}
      <Separador nome="Filmes populares hoje" />
      <DailyGrid tipo='movie'/>
      <CardsByGenre title={"Filmes da semana"} type={"movie"} />
      <Separador nome="Filmes em cartaz" />
      <div
        style={{
          width: '100%',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(407px, 407px))',
          gridGap: '10px',
          justifyContent: 'center',
          alignItems: 'center',
          flexWrap: 'wrap',
        }}
      >
        {movies.map(movie => (
          <Ticket
            key={movie.id}
            id={movie.id}
            title={movie.title}
            rate={(movie.vote_average.toFixed(1))/2}
            backDrop={`https://image.tmdb.org/t/p/original/${movie.backdrop_path}`}
            poster={`https://image.tmdb.org/t/p/w500/${movie.poster_path}`}
            DiaMes={`${movie.release_date.split('-')[2]}.${movie.release_date.split('-')[1]}`}
            ano={movie.release_date.split('-')[0]}
          />
        ))}
      </div>
    </div>
  );
}

export default Home;
