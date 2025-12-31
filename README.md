
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
    "I felt calm and happy, floating on a cloud",
    "A man chased me with a knife and nearly cut me!",
    "I couldn't believe she could betray me like that. But I forgave her and eventually felt peace."
  )
)

out <- score_croberta(
  test_df,
  text_col = "text",
  id_col   = "SubjectID",
  batch_size = 2
)

print(out)
```

### Output Example
```md

# A tibble: 3 × 6
  SubjectID text                                                       Joy  Fear Anger Sadness
      <dbl> <chr>                                                    <dbl> <dbl> <dbl>   <dbl>
1         1 I woke up feeling calm and happy after a peaceful dream. 0.712 0.320 0.295   0.346
2         2 The dream was terrifying and filled with panic.          0.183 0.811 0.432   0.679
3         3 I felt angry at first, but then relieved and safe.       0.410 0.531 0.377   0.471
```

