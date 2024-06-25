export interface Pasta {
  _id: number;
  title: string;
  body: string;
  timestamp: {
    $date: string;
  };
  updated_at: {
    $date: string;
  };
  overall_reactions: number;
  positive_reactions: number;
  negative_reactions: number;
  neutral_reactions: number;
  ratio: any;
  pasta_url: string;
  message_url: string;
  processed_text: {
    author: { author_name: string; author_url: string };
    body: string;
    date_published: string;
    page: number;
    title: string;
  };
}
