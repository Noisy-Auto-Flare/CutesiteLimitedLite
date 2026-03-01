import useSWR from 'swr';
import { api, Image, Video, Post } from './api';

const fetcher = (url: string) => api.get(url).then(res => res.data);

export function useImages() {
  const { data, error, mutate, isLoading } = useSWR<Image[]>('/images/', fetcher);
  return {
    images: data,
    isLoading,
    isError: error,
    mutate
  };
}

export function useVideos() {
  const { data, error, mutate, isLoading } = useSWR<Video[]>('/videos/', fetcher);
  return {
    videos: data,
    isLoading,
    isError: error,
    mutate
  };
}

export function usePosts() {
  const { data, error, mutate, isLoading } = useSWR<Post[]>('/posts/', fetcher);
  return {
    posts: data,
    isLoading,
    isError: error,
    mutate
  };
}
