#' Score text with local C-RoBERTa emotion intensity models
#'
#' @param data A data.frame/tibble containing a text column.
#' @param text_col Name of the column containing text.
#' @param id_col Optional ID column name (if absent, row index is used).
#' @param batch_size Batch size for inference.
#' @param envname Name of the reticulate virtualenv to use/create.
#' @param max_length Max token length for truncation.
#'
#' @return A tibble with the original id/text plus Joy/Fear/Anger/Sadness columns.
#' @export
score_croberta <- function(data,
                           text_col = "text",
                           id_col   = "SubjectID",
                           batch_size = 64L,
                           envname = "hf-env",
                           max_length = 128L) {
  stopifnot(is.data.frame(data))
  .ensure_croberta_env(envname)

  py_file <- system.file("python", "croberta_score.py", package = "crobertaR")
  reticulate::source_python(py_file)

  res <- score_df(
    df = data,
    batch_size = as.integer(batch_size),
    text_col = text_col,
    id_col = id_col,
    max_length = as.integer(max_length)
  )

  tibble::as_tibble(res)
}
