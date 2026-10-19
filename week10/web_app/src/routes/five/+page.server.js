export async function load() {
    const url = 'https://jsonplaceholder.typicode.com/posts'

    try {
        console.log('Fetch data from API')
        const response = await fetch(url)
        const posts = await response.json() 

        return {
            summaries: posts.map((post) => ({
                slug: post.id, 
                title: post.title,
            }))
        }
    } catch (error) {
        // @ts-ignore
        console.error(error.message)
    }
}