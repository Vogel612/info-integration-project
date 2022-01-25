package web.repository;

import web.controller.model.*;

import java.util.List;
import java.util.Set;

public interface AnimeRepository {

    List<AnimeTitle> getAllTitles();

    List<AnimeTitle> getTitlesRanked();

    String getTitleSynopsis(int titleId);

    List<AnimeTitle> getTitlesByYear(int from, int to);

    List<AnimeTitleWithWarnings> getTitlesWithoutContentWarnings(Set<String> warnings);

    List<AnimeTitleWithGenres> getTitlesByGenre(String genre);

    List<AnimeTitleWithProducers> getTitlesByProducer(String producer);

    List<AnimeTitleWithStudios> getTitlesByStudio(String studio);
}
