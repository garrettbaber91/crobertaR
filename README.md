
# crobertaR

Scores emotion intensity (Joy, Fear, Anger, and Sadness) from text using C-RoBERTa models via reticulate in R.

## Installation

```r
devtools::install_github("garrettbaber91/crobertaR")

```

## Example

This is a basic example which shows you how to solve a common problem:

``` r
library(crobertaR)
library(tibble)

test_df <- tibble(
  SubjectID = c(1, 2, 3),
  text = c(
    "I woke up feeling calm and happy after a peaceful dream.",
    "The dream was terrifying and filled with panic.",
    "I felt angry at first, but then relieved and safe."
  )
)

out <- score_croberta(
  test_df,
  text_col = "text",
  id_col   = "SubjectID",
  batch_size = 2
)

print(out)

# A tibble: 3 × 6
  SubjectID text                                                       Joy  Fear Anger Sadness
      <dbl> <chr>                                                    <dbl> <dbl> <dbl>   <dbl>
1         1 I woke up feeling calm and happy after a peaceful dream. 0.712 0.320 0.295   0.346
2         2 The dream was terrifying and filled with panic.          0.183 0.811 0.432   0.679
3         3 I felt angry at first, but then relieved and safe.       0.410 0.531 0.377   0.471
```

