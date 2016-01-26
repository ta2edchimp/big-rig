# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from collections import defaultdict


def GetChildPids(processes, pid):
  """Returns all child processes of |pid| from the given |processes| list.

  Args:
    processes: A tuple of (pid, ppid, state) as generated by ps.
    pid: The pid for which to get children.

  Returns:
    A list of child pids.
  """
  child_dict = defaultdict(list)
  for curr_pid, curr_ppid, state in processes:
    if 'Z' in state:
      continue  # Ignore zombie processes
    child_dict[int(curr_ppid)].append(int(curr_pid))
  queue = [pid]
  child_ids = []
  while queue:
    parent = queue.pop()
    if parent in child_dict:
      children = child_dict[parent]
      queue.extend(children)
      child_ids.extend(children)
  return child_ids


def GetPsOutputWithPlatformBackend(platform_backend, columns, pid):
  """Returns output of the 'ps' command as a list of lines.

  Args:
    platform_backend: The platform backend (LinuxBasedPlatformBackend or
        PosixPlatformBackend).
    columns: A list of require columns, e.g., ['pid', 'pss'].
    pid: If not None, returns only the information of the process with the pid.
  """
  args = ['ps']
  args.extend(['-p', str(pid)] if pid != None else ['-e'])
  for c in columns:
    args.extend(['-o', c + '='])
  return platform_backend.RunCommand(args).splitlines()