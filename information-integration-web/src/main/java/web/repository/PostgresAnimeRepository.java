package web.repository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;
import web.controller.model.AnimeTitle;
import web.controller.model.AnimeTitleWithGenres;
import web.controller.model.AnimeTitleWithWarnings;
import web.repository.mapper.AnimeRowMapper;
import web.repository.mapper.AnimeWithWarningRowMapper;

import java.util.List;
import java.util.Set;

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

    @Override
    public List<AnimeTitleWithWarnings> getTitlesWithContentWarnings(Set<String> warnings) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles at RIGHT JOIN result.content_warnings cw USING(id)",
                new AnimeWithWarningRowMapper());
    }

    @Override
    public List<AnimeTitleWithGenres> getTitlesByGenre(String genre) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles at LEFT JOIN result.anime_titles_genres USING(id)",
                new AnimeWithWarningRowMapper());
    }

    @Override
    public List<AnimeTitle> getTitlesByProducer(String producer) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles at LEFT JOIN result.anime_titles_producers USING(id)",
                new AnimeWithWarningRowMapper());
    }

    @Override
    public List<AnimeTitle> getTitlesByStudio(String studio) {
        return jdbcTemplate.query("SELECT * FROM result.anime_titles at LEFT JOIN result.anime_titles_studio USING(id)",
                new AnimeWithWarningRowMapper());
    }
}
