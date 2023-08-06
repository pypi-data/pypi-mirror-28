# Copyright 2016 AC Technologies LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Utilities for G2P trainer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib.learn.python.learn import learn_runner

from tensor2tensor.utils import devices
from tensor2tensor.utils import input_fn_builder
from tensor2tensor.utils import model_builder
from tensor2tensor.utils import registry
from tensor2tensor.utils import decoding
from tensor2tensor.utils import trainer_utils

flags = tf.flags
FLAGS = flags.FLAGS

flags.DEFINE_integer("save_checkpoints_steps", None,
    """Save checkpoints every this many steps. Default=None means let
    tensorflow.contrib.learn.python.learn decide, which saves checkpoints
    every 600 seconds.""")


def add_problem_hparams(hparams, problem_name, model_dir, problem_instance):
  """Add problem hparams for the problems."""
  hparams.problems = []
  hparams.problem_instances = []
  p_hparams = problem_instance.get_hparams(hparams)
  hparams.problem_instances.append(problem_instance)
  hparams.problems.append(p_hparams)


def create_experiment_components(params, hparams, run_config,
                                 problem_instance,
                                 train_preprocess_file_path=None,
                                 dev_preprocess_file_path=None):
  """Constructs and returns Estimator and train/eval input functions."""
  tf.logging.info("Creating experiment, storing model files in %s",
                  run_config.model_dir)

  add_problem_hparams(hparams, params.problem_name, params.model_dir,
                      problem_instance)

  # hparams batch_size is used as minibatch size instead of tokens in batch
  batch_size = (hparams.use_fixed_batch_size and hparams.batch_size) or None
  num_datashards = 1
  train_input_fn = input_fn_builder.build_input_fn(
      mode=tf.estimator.ModeKeys.TRAIN,
      hparams=hparams,
      data_dir=params.data_dir,
      num_datashards=num_datashards,
      worker_replicas=FLAGS.worker_replicas,
      worker_id=FLAGS.worker_id,
      batch_size=batch_size,
      dataset_split=train_preprocess_file_path)

  eval_input_fn = input_fn_builder.build_input_fn(
      mode=tf.estimator.ModeKeys.EVAL,
      hparams=hparams,
      data_dir=params.data_dir,
      num_datashards=num_datashards,
      worker_replicas=FLAGS.worker_replicas,
      worker_id=FLAGS.worker_id,
      dataset_split=dev_preprocess_file_path)

  model_fn = model_builder.build_model_fn(
      params.model_name,
      problem_names=[params.problem_name],
      train_steps=params.train_steps,
      worker_id=FLAGS.worker_id,
      worker_replicas=FLAGS.worker_replicas,
      eval_run_autoregressive=FLAGS.eval_run_autoregressive,
      decode_hparams=decoding.decode_hparams(params.decode_hparams))

  estimator = tf.estimator.Estimator(
      model_fn=model_fn,
      model_dir=run_config.model_dir,
      params=hparams,
      config=run_config)

  return estimator, {
      tf.estimator.ModeKeys.TRAIN: train_input_fn,
      tf.estimator.ModeKeys.EVAL: eval_input_fn}


def make_experiment_fn(params, problem_instance, train_preprocess_file_path,
                       dev_preprocess_file_path):
  """Returns experiment_fn for learn_runner. Wraps create_experiment."""

  def experiment_fn(run_config, hparams):
    """Function for running experiment creation."""
    return create_experiment(
        params,
        hparams=hparams,
        run_config=run_config,
        problem_instance=problem_instance,
        train_preprocess_file_path=train_preprocess_file_path,
        dev_preprocess_file_path=dev_preprocess_file_path)

  return experiment_fn


def create_experiment(params, hparams, run_config, problem_instance,
                      train_preprocess_file_path,
                      dev_preprocess_file_path):
  """Create Experiment."""
  estimator, input_fns = create_experiment_components(
      params=params,
      hparams=hparams,
      run_config=run_config,
      problem_instance=problem_instance,
      train_preprocess_file_path=train_preprocess_file_path,
      dev_preprocess_file_path=dev_preprocess_file_path)

  train_monitors = []
  eval_hooks = []
  if FLAGS.dbgprofile:
    # Recorded traces can be visualized with chrome://tracing/
    # The memory/tensor lifetime is also profiled
    train_monitors.append(
        tf.contrib.hooks.ProfilerHook(
            save_steps=10,
            output_dir=run_config.model_dir,
            show_dataflow=True,
            show_memory=True,
        ))
  if params.schedule == "train_and_evaluate":
    if FLAGS.local_eval_frequency:
      train_monitors.append(
          tf.contrib.learn.monitors.ValidationMonitor(
              input_fn=input_fns[tf.estimator.ModeKeys.EVAL],
              eval_steps=params.eval_steps,
              every_n_steps=FLAGS.local_eval_frequency,
              hooks=eval_hooks,
              early_stopping_rounds=FLAGS.eval_early_stopping_steps,
              early_stopping_metric=FLAGS.eval_early_stopping_metric,
              early_stopping_metric_minimize=FLAGS.
              eval_early_stopping_metric_minimize))

  return tf.contrib.learn.Experiment(
      estimator=estimator,
      train_input_fn=input_fns[tf.estimator.ModeKeys.TRAIN],
      eval_input_fn=input_fns[tf.estimator.ModeKeys.EVAL],
      train_steps=params.train_steps,
      eval_steps=params.eval_steps,
      train_monitors=train_monitors,
      eval_hooks=eval_hooks,
      eval_delay_secs=0)


def create_run_config(output_dir):
  """Create a RunConfig object."""

  FLAGS.keep_checkpoint_max = 1

  run_config = tf.contrib.learn.RunConfig(
      model_dir=output_dir,
      master=FLAGS.master,
      gpu_memory_fraction=FLAGS.worker_gpu_memory_fraction,
      session_config=trainer_utils.session_config(),
      keep_checkpoint_max=FLAGS.keep_checkpoint_max,
      keep_checkpoint_every_n_hours=FLAGS.keep_checkpoint_every_n_hours,
      save_checkpoints_steps=FLAGS.save_checkpoints_steps)

  return run_config


def run(params, problem_instance, train_preprocess_file_path,
        dev_preprocess_file_path):
  """Runs an Estimator locally or distributed.

  Args:
    data_dir: The directory the data can be found in.
    model_name: The name of the model to use.
    output_dir: The directory to store outputs in.
    train_steps: The number of steps to run training for.
    eval_steps: The number of steps to run evaluation for.
    schedule: (str) The schedule to run. The value here must
      be the name of one of Experiment's methods.
  """
  exp_fn = make_experiment_fn(
      params,
      problem_instance,
      train_preprocess_file_path=train_preprocess_file_path,
      dev_preprocess_file_path=dev_preprocess_file_path)

  # Create hparams and run_config
  #run_config = trainer_utils.create_run_config(params.model_dir)
  run_config = create_run_config(params.model_dir)
  hparams = trainer_utils.create_hparams(
      params.hparams_set,
      params.data_dir,
      passed_hparams=params.hparams)

  if trainer_utils.is_chief():
    trainer_utils.save_metadata(params.model_dir, hparams)

  learn_runner.run(
      experiment_fn=exp_fn,
      schedule=params.schedule,
      run_config=run_config,
      hparams=hparams)
