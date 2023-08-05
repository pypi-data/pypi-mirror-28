# -*- coding: utf-8 -*-

"""Console script for mcli."""

import os
import re
import json
import click
import requests as r



class MarketMakerCLI(click.MultiCommand):
    _url = 'http://127.0.0.1:7783/'
    _home_folder = os.environ.get('HOME')
    _userpass_file = 'SuperNET/iguana/dexscripts/userpass'
    commands = {}

    def _get_userpass(self):
        file = open(os.path.join(self._home_folder,self._userpass_file), 'r')
        for line in file:
            userpass = re.search('export userpass="(.*?)"', line).group(1)
            return userpass
    
    def get_mm_help(self):
        commands = self._call_marketmaker('help', {})
        commands = json.loads(commands.text.replace('\n', ''))['result']
        commands = re.findall('([a-z]*\(.*?\))', commands)
        return commands
    
    def get_commands(self):
        commands = {}
        for command in self.get_mm_help():
            definition = re.search('([a-z]+)(:?\(.*?\))', command)
            method_name = definition.group(1)
            commands[method_name] = None
            params = definition.group(2).replace('(', '').replace(')', '').split(',')
            commands[method_name] = params
        self.commands = commands
        return commands

    def list_commands(self, ctx):
        rv = list(self.get_commands().keys())
        rv.sort()
        return rv
    
    def _call_marketmaker(self, method, params):
        params = dict(filter(lambda item: item[1] is not None, params.items()))
        params['method'] = method
        params['userpass'] = self._get_userpass()
        response = r.post(self._url, data=json.dumps(params))
        return response

    def get_command(self, ctx, name):
        ns = {}
        parameters = []
        for command, params in self.get_commands().items():
            if command == name:
                for param in params:
                    param = re.search('([a-z]+)', param)
                    if param:
                        param_string = '--'+param.group(0)
                        parameters.append(click.Option((param_string,),))

        @click.pass_context
        def callback(*args, **kwargs):
            output = self._call_marketmaker(name, kwargs)
            click.echo(json.dumps(output.json(), indent=2))
        ret = click.Command(name, params=parameters, callback=callback)
        return ret

@click.command(cls=MarketMakerCLI)
@click.pass_context
def main(ctx, *args, **kvargs):
   pass

if __name__ == "__main__":
    main()
