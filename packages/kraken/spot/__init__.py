#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that provides the Spot REST clients and utility functions."""

# pylint: disable=unused-import
from packages.kraken.spot.funding import Funding
from packages.kraken.spot.market import Market
from packages.kraken.spot.orderbook import OrderbookClient
from packages.kraken.spot.staking import Staking
from packages.kraken.spot.trade import Trade
from packages.kraken.spot.user import User
from packages.kraken.spot.ws_client import KrakenSpotWSClient
