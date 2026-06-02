export interface Variation {
  id: number
  merchandise_id: number
  quantity: number
  price: number
  variation_text: string
  weight_gram: number
}

export interface Merchandise {
  id: number
  category_id: number
  name: string
  description: string
  image: string
  variations: Variation[]
}

export interface Category {
  id: number
  name: string
  slug: string
  description: string
  merchandises: Merchandise[]
}