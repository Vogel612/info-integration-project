package web.repository.mapper;

import org.springframework.jdbc.core.RowMapper;
import web.controller.model.AnimeTitleWithGenres;
import web.controller.model.AnimeTitleWithWarnings;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class AnimeWithGenresRowMapper implements RowMapper<AnimeTitleWithGenres> {

    @Override
    public AnimeTitleWithGenres mapRow(ResultSet rs, int rowNum) throws SQLException {
        List<String> genres = Arrays.stream(((String[]) rs.getArray("genres").getArray())).collect(Collectors.toList());

        return new AnimeTitleWithGenres(
                rs.getInt("id"), rs.getString("title"), rs.getInt("duration"),
                rs.getInt("number_of_episodes"), rs.getString("media_type"),
                rs.getFloat("score"), rs.getString("source"), rs.getInt("start_year"),
                rs.getInt("finish_year"), rs.getString("season_of_release"), genres
        );
    }
}
