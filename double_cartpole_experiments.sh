#!//usr/bin/env bash

OPTS="-r True -o /localdata/juan/iclr2018"
#OPTS="-o /localdata/juan/iclr2018"
#EXTRA_OPTS="-k mc_samples 100 -k max_evals 1000 -k learning_rate 1e-3 -k polyak_averaging None -k clip_gradients 1.0 -k heteroscedastic_dyn True -k debug_plot 1 -k n_opt 50"
EXTRA_OPTS="-k mc_samples 100 -k max_evals 1000 -k learning_rate 1e-3 -k polyak_averaging None -k clip_gradients 1.0 -k heteroscedastic_dyn True -k debug_plot 0 -k n_opt 50"

python examples/PILCO/double_cartpole_learn.py -e 1 -n dcp_pilco_ssgp_rbfp ${OPTS} ${EXTRA_OPTS}
python examples/PILCO/double_cartpole_learn.py -e 3 -n dcp_mcpilco_dropoutd_rbfp ${OPTS} ${EXTRA_OPTS}
python examples/PILCO/double_cartpole_learn.py -e 4 -n dcp_mcpilco_dropoutd_mlpp ${OPTS} ${EXTRA_OPTS}
python examples/PILCO/double_cartpole_learn.py -e 5 -n dcp_mcpilco_lndropoutd_rbfp ${OPTS} ${EXTRA_OPTS}
python examples/PILCO/double_cartpole_learn.py -e 6 -n dcp_mcpilco_lndropoutd_mlpp ${OPTS} ${EXTRA_OPTS}
python examples/PILCO/double_cartpole_learn.py -e 7 -n dcp_mcpilco_dropoutd_dropoutp ${OPTS} ${EXTRA_OPTS}
python examples/PILCO/double_cartpole_learn.py -e 8 -n dcp_mcpilco_lndropoutd_dropoutp ${OPTS} ${EXTRA_OPTS}
