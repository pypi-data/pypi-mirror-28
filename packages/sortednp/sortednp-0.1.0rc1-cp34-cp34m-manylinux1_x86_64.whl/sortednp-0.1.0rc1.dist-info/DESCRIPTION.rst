Numpy and Numpy arrays are a really great tool. However, intersecting
and merging multiple numpy arrays is rather less performant. The current
numpy implementation concatenates the two arrays and sorts the
combination. If you want to merge or intersect multiple numpy arrays,
there is a much faster way, by using the property, that the resulting
array is sorted.

Sortednp (sorted numpy) operates on sorted numpy arrays to calculate the
intersection or the union of two numpy arrays in an efficient way. The
resulting array is again a sorted numpy array, which can be merged or
intersected with the next array. The intended use case is that sorted
numpy arrays are sorted as the basic data structure and merged or
intersected at request. Typical applications include information
retrieval and search engines in particular.

