import gevent.monkey
gevent.monkey.patch_all()

import wikipedia as wk
import markovify

wk.set_rate_limiting(True)

topic = 'wikipedia'
depth = 2
input_path = './wiki_input.txt'
output_path = './wiki_output.txt'
paragraphs = 4
sentences = 10


def load_data(topic):
    def load_page(title, queue, visited):
        try:
            visited.add(title)
            page = wk.page(title)
            text = ' '.join(line.replace('.', '. ').replace('  ', ' ') for line in page.content.split('\n') if
                            line and not line.startswith('='))
            if topic.lower() in text.lower():
                print(title)
                file.write(text)
                for link in page.links:
                    if link not in visited:
                        queue.add(link)
        except wk.WikipediaException as err:
            print(title, '::', err)
    
    visited = set()
    page_queue = wk.search(topic)
    article_ct = 0
    with open(input_path, 'w+', encoding='utf8') as file:
        for i in range(depth):
            batch = page_queue[:100]
            queue = {*page_queue[100:]}
            gevent.wait([gevent.spawn(load_page, title, queue, visited) for title in batch])
            article_ct += len(batch)
            page_queue = [*queue]
    print('Articles parsed:', len(visited), '/', article_ct)


def create_chain():
    with open(input_path, 'r', encoding='utf8') as file:
        text = file.read()
    
    model = markovify.Text(text, state_size=3)
    output_lines = []
    for i in range(paragraphs):
        output_lines.append(' '.join(s for s in (model.make_sentence() for _ in range(sentences)) if s))
    
    output = '\n'.join(line + '\n' for line in output_lines)
    with open(output_path, 'w+', encoding='utf8') as file:
        file.write(output)
    # print(output)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Create nonsensical essays about a particular topic.')
    parser.add_argument('topic', metavar='T', help='essay topic')
    parser.add_argument('--depth', type=int, help='article search depth')
    parser.add_argument('--paragraphs', type=int, help='paragraphs per essay')
    parser.add_argument('--sentences', type=int, help='sentences per paragraph')
    args = parser.parse_args()
    
    topic = args.topic
    depth = args.depth or depth
    paragraphs = args.paragraphs or paragraphs
    sentences = args.sentences or sentences
    
    load_data(topic)
    create_chain()
