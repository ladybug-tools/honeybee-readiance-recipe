"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import os
import pathlib
from queenbee_local import QueenbeeTask
from .dependencies.direct_sun_hours_entry_loop import _DirectSunHoursEntryLoop_3edc04c8Orchestrator as DirectSunHoursEntryLoop_3edc04c8Workerbee


_default_inputs = {   'grid_filter': '*',
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'sensor_count': 200,
    'simulation_folder': '.',
    'timestep': 1,
    'wea': None}


class ConvertWeaToConstant(QueenbeeTask):
    """Convert a Wea file to have a constant value for each datetime.

    This is useful in workflows where hourly irradiance values are inconsequential
    to the analysis and one is only using the Wea as a format to pass location
    and datetime information (eg. for direct sun hours)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    value = luigi.Parameter(default='1000')

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'ladybug translate wea-to-constant weather.wea --value {value} --output-file constant.wea'.format(value=self.value)

    def output(self):
        return {
            'constant_wea': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/constant.wea').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'weather.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'constant-wea', 'from': 'constant.wea',
                'to': pathlib.Path(self.execution_folder, 'resources/constant.wea').resolve().as_posix()
            }]


class CopyGridInfo(QueenbeeTask):
    """Copy a file or folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/cumulative/grids_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'results/cumulative/grids_info.json').resolve().as_posix()
            }]


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder and a sky!"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out} --add-before sky.sky'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/scene_with_suns.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sky', 'to': 'sky.sky', 'from': self.sky, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'resources/scene_with_suns.oct').resolve().as_posix()
            }]


class CreateRadFolder(QueenbeeTask):
    """Create a Radiance folder from a HBJSON input file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def input_model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid "{grid_filter}" --grid-check'.format(grid_filter=self.grid_filter)

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'bsdf_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix()
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/direct_sun_hours/grids_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'model/grid/_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_model', 'to': 'model.hbjson', 'from': self.input_model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            },
                
            {
                'name': 'bsdf-folder', 'from': 'model/bsdf',
                'to': pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix()
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'model/grid/_info.json',
                'to': pathlib.Path(self.execution_folder, 'results/direct_sun_hours/grids_info.json').resolve().as_posix()
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'model/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'model/grid/_info.json').resolve().as_posix()}]


class DirectSunHoursRaytracingLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def timestep(self):
        return self._input_params['timestep']

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['CreateOctree']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path, 'grid/{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sunpath(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        try:
            pathlib.Path(self.input()['CreateRadFolder']['bsdf_folder'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CreateRadFolder']['bsdf_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_name}'.format(item_name=self.item['name'])).resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'timestep': self.timestep,
            'sensor_count': self.sensor_count,
            'octree_file': self.octree_file,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'sunpath': self.sunpath,
            'sun_modifiers': self.sun_modifiers,
            'bsdfs': self.bsdfs
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DirectSunHoursEntryLoop_3edc04c8Workerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'direct_sun_hours_raytracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateOctree': CreateOctree(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'direct_sun_hours_raytracing.done').resolve().as_posix())
        }


class DirectSunHoursRaytracing(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['CreateRadFolder']['sensor_grids'].path).as_posix()

    def run(self):
        yield [DirectSunHoursRaytracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'direct_sun_hours_raytracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateOctree': CreateOctree(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'direct_sun_hours_raytracing.done').resolve().as_posix())
        }


class GenerateSunpath(QueenbeeTask):
    """Generate a Radiance sun matrix (AKA sun-path)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def output_type(self):
        return '1'

    @property
    def wea(self):
        value = pathlib.Path(self.input()['ConvertWeaToConstant']['constant_wea'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'gendaymtx -n -D sunpath.mtx -M suns.mod -O{output_type} -r {north} -v sky.wea'.format(output_type=self.output_type, north=self.north)

    def requires(self):
        return {'ConvertWeaToConstant': ConvertWeaToConstant(_input_params=self._input_params)}

    def output(self):
        return {
            'sunpath': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sunpath.mtx').resolve().as_posix()
            ),
            
            'sun_modifiers': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/suns.mod').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sunpath', 'from': 'sunpath.mtx',
                'to': pathlib.Path(self.execution_folder, 'resources/sunpath.mtx').resolve().as_posix()
            },
                
            {
                'name': 'sun-modifiers', 'from': 'suns.mod',
                'to': pathlib.Path(self.execution_folder, 'resources/suns.mod').resolve().as_posix()
            }]


class ParseSunUpHours(QueenbeeTask):
    """Parse sun up hours from sun modifiers file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    leap_year = luigi.Parameter(default='full-year')

    timestep = luigi.Parameter(default='1')

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sunpath parse-hours suns.mod --name sun-up-hours.txt --timestep {timestep} --{leap_year}'.format(timestep=self.timestep, leap_year=self.leap_year)

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params)}

    def output(self):
        return {
            'sun_up_hours': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/direct_sun_hours/sun-up-hours.txt').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sun_modifiers', 'to': 'suns.mod', 'from': self.sun_modifiers, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sun-up-hours', 'from': 'sun-up-hours.txt',
                'to': pathlib.Path(self.execution_folder, 'results/direct_sun_hours/sun-up-hours.txt').resolve().as_posix()
            }]


class _Main_3edc04c8Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CopyGridInfo(_input_params=self.input_values), DirectSunHoursRaytracing(_input_params=self.input_values), ParseSunUpHours(_input_params=self.input_values)]
