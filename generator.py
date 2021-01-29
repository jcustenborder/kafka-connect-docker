import json
import os.path
import re
import urllib.request
from os import path

import yaml

settings = None

with open('images.yml') as imagesFile:
    settings = yaml.load(imagesFile, Loader=yaml.FullLoader)

output_root = settings['output']

if not path.exists(output_root):
    print(f"Creating output path: {output_root}")
    os.mkdir(output_root)

hub_cache = {}


def api_plugins(api_owner):
    owner_url = f"https://api.hub.confluent.io/api/plugins/{api_owner}"
    result = None
    if owner_url in hub_cache:
        print(f"Using cache {owner_url}")
        result = hub_cache[owner_url]
    else:
        print(f"Downloading {owner_url}")
        with urllib.request.urlopen(owner_url) as url:
            result = json.loads(url.read().decode())
            hub_cache[owner_url] = result
    return result


def api_plugin(api_owner, api_name):
    plugin_url = f"https://api.hub.confluent.io/api/plugins/{api_owner}/{api_name}"
    result = None
    if plugin_url in hub_cache:
        print(f"Using cache {plugin_url}")
        result = hub_cache[plugin_url]
    else:
        print(f"Downloading {plugin_url}")
        with urllib.request.urlopen(plugin_url) as url:
            result = json.loads(url.read().decode())
            hub_cache[plugin_url] = result
    return result


repositories = []
repositories_file_path = path.join(output_root, 'repositories.json')

for image, imageSettings in settings['images'].items():
    print(f"Processing {image}")
    image_root = path.join(output_root, image)
    from_image = imageSettings['image']

    if not path.exists(image_root):
        os.mkdir(image_root)

    for image_version, base_image_version in imageSettings['versions'].items():
        version_root = path.join(image_root, image_version)

        repository = {
            'name': image,
            'path': version_root,
            'branch': image_version,
            'repository_url': imageSettings['repository']
        }
        repositories.append(repository)
        if not path.exists(version_root):
            os.mkdir(version_root)

        docker_file_path = path.join(version_root, "Dockerfile")
        readme_file_path = path.join(version_root, "README.md")

        download_plugins = {}
        if 'plugins' in imageSettings:
            for plugin in imageSettings['plugins']:
                owner = plugin['owner']
                plugin = plugin['plugin']
                hub_contents = api_plugins(owner)

                for hub_plugin in hub_contents:
                    plugin_name = hub_plugin['name']
                    if re.match(plugin, plugin_name):
                        plugin_info = api_plugin(owner, plugin_name)
                        download_plugins[f"{owner}/{plugin_name}"] = plugin_info

        with open(docker_file_path, "+w") as dockerFile:
            print(f"FROM {from_image}:{base_image_version}", file=dockerFile)

            if 'labels' in settings:
                for key, value in sorted(settings['labels'].items()):
                    print(f"LABEL {key}=\"{value}\"", file=dockerFile)

            if 'env' in imageSettings:
                for key, value in imageSettings['env'].items():
                    print(f"ENV {key}={value}", file=dockerFile)

            for download_plugin, plugin_info in sorted(download_plugins.items()):
                print(
                    f"RUN confluent-hub install --no-prompt {download_plugin}:{plugin_info['version']}",
                    file=dockerFile)

        with open(readme_file_path, "+w") as readmeFile:
            if 'readme' in imageSettings:
                for header, content in imageSettings['readme'].items():
                    print(f"# {header}\n", file=readmeFile)
                    print(f"{content}", file=readmeFile)

            print("", file=readmeFile)
            print("| Plugin | Version | Documentation | Source |", file=readmeFile)
            print("|--------|---------|---------------|--------|", file=readmeFile)

            for download_plugin, plugin_info in sorted(download_plugins.items()):
                hub_url = f"https://www.confluent.io/hub/{download_plugin}"

                print(
                    f"| [{download_plugin}]({hub_url}) | {plugin_info['version']} | [Documentation]({plugin_info['documentation_url']}) | [Source]({plugin_info['source_url']}) |",
                    file=readmeFile)

with open(repositories_file_path, "+w") as repositories_file:
    repositories_file.write(json.dumps(repositories, indent=4))
