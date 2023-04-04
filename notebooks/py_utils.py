from duckduckgo_search import ddg_images
from fastcore.foundation import L


def search_images(term, max_images=200):
    return L(ddg_images(term, max_results=max_images)).itemgot('image')


categories = (
    'Dall-E', 'Midjourney' 'Stable Diffusion',
)

search_terms = (
    'Generated with %s',
)
# flat list of search terms for each category
search_terms = [search_term % category for category in categories for search_term in search_terms]