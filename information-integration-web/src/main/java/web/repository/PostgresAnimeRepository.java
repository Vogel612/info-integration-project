package web.repository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;
import web.controller.model.*;
import web.repository.mapper.*;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Repository
public class PostgresAnimeRepository implements AnimeRepository {
    private static final RowMapper<AnimeTitle> ANIME_TITLE_ROW_MAPPER = new AnimeRowMapper();

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public List<AnimeTitle> getAllTitles() {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles", ANIME_TITLE_ROW_MAPPER);
    }

    @Override
    public List<AnimeTitle> getTitlesRanked() {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles ORDER BY score", ANIME_TITLE_ROW_MAPPER);
    }

    @Override
    public String getTitleSynopsis(int titleId) {
        return jdbcTemplate.queryForObject("SELECT synopsis FROM result.anime_titles WHERE id = ?", String.class, titleId);
    }

    @Override
    public List<AnimeTitle> getTitlesByYear(int from, int to) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles WHERE start_year > ? AND start_year < ?",
                ANIME_TITLE_ROW_MAPPER, from, to);
    }

    // todo - group by for below queries
    @Override
    public List<AnimeTitleWithWarnings> getTitlesWithoutContentWarnings(Set<String> warnings) {
        List<AnimeTitleWithWarnings> animeTitleWithWarnings = jdbcTemplate.query("SELECT * FROM result.anime_titles at " +
                "LEFT JOIN result.anime_titles_content_warnings atcw ON at.id = atcw.anime_title_id " +
                "LEFT JOIN result.content_warnings cw on atcw.content_warning_id = cw.id", new AnimeWithWarningRowMapper());

        return animeTitleWithWarnings.stream()
                .filter(anime -> anime.getWarnings().stream().noneMatch(warnings::contains))
                .collect(Collectors.toList());
    }

    @Override
    public List<AnimeTitleWithGenres> getTitlesByGenre(String genre) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles at " +
                "LEFT JOIN result.anime_titles_genres atg ON at.id = atg.anime_title_id " +
                "LEFT JOIN result.genres g ON atg.genre_id = g.id " +
                "WHERE genre = ?", new AnimeWithGenresRowMapper(), genre);
    }

    @Override
    public List<AnimeTitleWithProducers> getTitlesByProducer(String producer) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles at " +
                "LEFT JOIN result.anime_titles_producers atp ON at.id = atp.anime_title_id " +
                "LEFT JOIN result.producers p ON atp.producer_id = p.id " +
                "WHERE producer = ?", new AnimeWithProducersRowMapper(), producer);
    }

    @Override
    public List<AnimeTitleWithStudios> getTitlesByStudio(String studio) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles at " +
                "LEFT JOIN result.anime_titles_studios ats ON at.id = ats.anime_title_id " +
                "LEFT JOIN result.studios s on ats.studio_id = s.id " +
                "WHERE studio = ?", new AnimeWithStudiosRowMapper(), studio);
    }
}
