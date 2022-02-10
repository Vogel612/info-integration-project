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
    private static final String TITLES_SQL = "select * from public.anime_titles_merged at " +
            "left join (select atcw.id, array_agg(warning) as warning from public.anime_titles_content_warnings_merged atcw " +
            "left join public.content_warnings cw on atcw.content_warning_id = cw.id " +
            "group by atcw.id) cw on at.id = cw.id " +
            "left join (select atg.id, array_agg(genre) as genre from public.anime_titles_genres_merged atg " +
            "left join public.genres g on atg.genre_id = g.id " +
            "group by atg.id) g on at.id = g.id " +
            "left join (select atp.id, array_agg(producer) as producer from public.anime_titles_producers_merged atp " +
            "left join public.producers p on atp.producer_id = p.id " +
            "group by atp.id) p on at.id = p.id " +
            "left join (select ats.id, array_agg(studio) as studio from public.anime_titles_studios_merged ats " +
            "left join public.studios s on ats.studio_id = s.id " +
            "group by ats.id) s on at.id = s.id";
    
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public List<AnimeTitle> getAllTitles() {
        return jdbcTemplate.query(TITLES_SQL, ANIME_TITLE_ROW_MAPPER);
    }

    @Override
    public List<AnimeTitle> getTitlesRanked() {
        return jdbcTemplate.query(TITLES_SQL + " where score is not null order by score desc", ANIME_TITLE_ROW_MAPPER);
    }

    @Override
    public String getTitleSynopsis(int titleId) {
        return jdbcTemplate.queryForObject("SELECT synopsis FROM public.anime_titles_merged WHERE id = ?", String.class, titleId);
    }

    @Override
    public List<AnimeTitle> getTitlesByYear(int from, int to) {
        return jdbcTemplate.query(TITLES_SQL + " where start_year > ? and finish_year < ? and score is not null order by score desc",
                ANIME_TITLE_ROW_MAPPER, from, to);
    }

    @Override
    public List<AnimeTitle> getTitlesWithoutContentWarnings(Set<String> warnings) {
        List<AnimeTitle> animeTitleWithWarnings = jdbcTemplate.query(TITLES_SQL + " where score is not null order by score desc",
                ANIME_TITLE_ROW_MAPPER);

        return animeTitleWithWarnings.stream()
                .filter(anime -> Arrays.stream(anime.getContentWarnings()).noneMatch(warnings::contains))
                .collect(Collectors.toList());
    }

    @Override
    public List<AnimeTitle> getTitlesByGenre(String genre) {
        return jdbcTemplate.query(TITLES_SQL + " WHERE ? = ANY(genre) and score is not null order by score desc",
                ANIME_TITLE_ROW_MAPPER, genre);
    }

    @Override
    public List<AnimeTitle> getTitlesByProducer(String producer) {
        return jdbcTemplate.query(TITLES_SQL + " WHERE ? = ANY(producer) and score is not null order by score desc",
                ANIME_TITLE_ROW_MAPPER, producer);
    }

    @Override
    public List<AnimeTitle> getTitlesByStudio(String studio) {
        return jdbcTemplate.query(TITLES_SQL + " WHERE ? = ANY(studio) and score is not null order by score desc", ANIME_TITLE_ROW_MAPPER, studio);
    }

    @Override
    public List<AnimeTitle> getTitlesWithSpecificDuration(int duration, int episodes) {
        return jdbcTemplate.query(TITLES_SQL + " WHERE duration_in_minutes <= ? and number_of_episodes <= ? and score is not null order by score desc",
                ANIME_TITLE_ROW_MAPPER, duration, episodes);
    }

    @Override
    public List<AnimeTitle> getUndiscoveredTitles() {
        return jdbcTemplate.query(TITLES_SQL + " WHERE score is null", ANIME_TITLE_ROW_MAPPER);
    }
}
