package web.repository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;
import web.controller.model.AnimeTitle;
import web.repository.mapper.AnimeRowMapper;

import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Repository
public class PostgresAnimeRepository implements AnimeRepository {
    private static final RowMapper<AnimeTitle> ANIME_TITLE_ROW_MAPPER = new AnimeRowMapper();
    private static final String TITLES_SQL = "select * from result.anime_titles at " +
            "left join (select anime_title_id, array_agg(warning) as warning from result.anime_titles_content_warnings atcw " +
            "left join result.content_warnings cw on atcw.content_warning_id = cw.id " +
            "group by anime_title_id) cw on at.id = cw.anime_title_id " +
            "left join (select anime_title_id, array_agg(genre) as genre from result.anime_titles_genres atg " +
            "left join result.genres g on atg.genre_id = g.id " +
            "group by anime_title_id) g on at.id = g.anime_title_id " +
            "left join (select anime_title_id, array_agg(producer) as producer from result.anime_titles_producers atp " +
            "left join result.producers p on atp.producer_id = p.id " +
            "group by anime_title_id) p on at.id = p.anime_title_id " +
            "left join (select anime_title_id, array_agg(studio) as studio from result.anime_titles_studios ats " +
            "left join result.studios s on ats.studio_id = s.id " +
            "group by anime_title_id) s on at.id = s.anime_title_id";

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public List<AnimeTitle> getAllTitles() {
        return jdbcTemplate.query(TITLES_SQL, ANIME_TITLE_ROW_MAPPER);
    }

    @Override
    public List<AnimeTitle> getTitlesRanked() {
        return jdbcTemplate.query(TITLES_SQL + " order by score", ANIME_TITLE_ROW_MAPPER);
    }

    @Override
    public String getTitleSynopsis(int titleId) {
        return jdbcTemplate.queryForObject("SELECT synopsis FROM result.anime_titles WHERE id = ?", String.class, titleId);
    }

    @Override
    public List<AnimeTitle> getTitlesByYear(int from, int to) {
        return jdbcTemplate.query(TITLES_SQL + " where start_year > ? and start_year < ?", ANIME_TITLE_ROW_MAPPER, from, to);
    }

    @Override
    public List<AnimeTitle> getTitlesWithoutContentWarnings(Set<String> warnings) {
        List<AnimeTitle> animeTitleWithWarnings = jdbcTemplate.query(TITLES_SQL, ANIME_TITLE_ROW_MAPPER);

        return animeTitleWithWarnings.stream()
                .filter(anime -> Arrays.stream(anime.getContentWarnings()).noneMatch(warnings::contains))
                .collect(Collectors.toList());
    }

    @Override
    public List<AnimeTitle> getTitlesByGenre(String genre) {
        return jdbcTemplate.query(TITLES_SQL + " WHERE ? = ANY(genre)", ANIME_TITLE_ROW_MAPPER, genre);
    }

    @Override
    public List<AnimeTitle> getTitlesByProducer(String producer) {
        return jdbcTemplate.query(TITLES_SQL + " WHERE ? = ANY(producer)", ANIME_TITLE_ROW_MAPPER, producer);
    }

    @Override
    public List<AnimeTitle> getTitlesByStudio(String studio) {
        return jdbcTemplate.query(TITLES_SQL + " WHERE ? = ANY(studio)", ANIME_TITLE_ROW_MAPPER, studio);
    }
}
