#' Ensure python environment for croberta scoring
#' @keywords internal
.ensure_croberta_env <- function(envname = "hf-env") {
  if (!reticulate::virtualenv_exists(envname)) {
    reticulate::virtualenv_create(envname)
    reticulate::virtualenv_install(
      envname,
      packages = c("torch", "transformers", "pandas"),
      ignore_installed = FALSE
    )
  }
  reticulate::use_virtualenv(envname, required = TRUE)
}
