package web.repository.mapper;

import org.springframework.jdbc.core.RowMapper;
import web.controller.model.AnimeTitle;

import java.sql.Array;
import java.sql.ResultSet;
import java.sql.SQLException;

public class AnimeRowMapper implements RowMapper<AnimeTitle> {

    @Override
    public AnimeTitle mapRow(ResultSet rs, int rowNum) throws SQLException {
        return new AnimeTitle(
                rs.getInt("id"), rs.getString("title"), rs.getInt("duration_in_minutes"),
                rs.getInt("number_of_episodes"), rs.getString("media_type"),
                rs.getFloat("score"), rs.getString("source"), rs.getInt("start_year"),
                rs.getInt("finish_year"), rs.getString("season_of_release"),
                getArrayNullSafe(rs, "warning"),
                getArrayNullSafe(rs, "genre"),
                getArrayNullSafe(rs, "producer"),
                getArrayNullSafe(rs, "studio")
        );
    }

    private String[] getArrayNullSafe(ResultSet resultSet, String column) throws SQLException {
        Array warning = resultSet.getArray(column);
        String[] result = new String[0];
        if (warning != null) {
            result = (String[]) warning.getArray();
        }
        return result;
    }
}
