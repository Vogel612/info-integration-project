package web.repository;

import web.controller.model.*;

import java.util.List;
import java.util.Set;

public interface AnimeRepository {

    List<AnimeTitle> getAllTitles();

    List<AnimeTitle> getTitlesRanked();

    String getTitleSynopsis(int titleId);

    List<AnimeTitle> getTitlesByYear(int from, int to);

    List<AnimeTitle> getTitlesWithoutContentWarnings(Set<String> warnings);

    List<AnimeTitle> getTitlesByGenre(String genre);

    List<AnimeTitle> getTitlesByProducer(String producer);

    List<AnimeTitle> getTitlesByStudio(String studio);
}
