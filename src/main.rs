
extern crate irc;
extern crate regex;
extern crate hyper;

mod at;
mod plugins;

use std::path::Path;
use irc::client::prelude::*;

use at::{AtRust, AtTrigger};


fn deneme(trigger: &AtTrigger, at: &AtRust) {
    at.say(trigger, "merhaba");
    at.reply(trigger, "merhaba");
}

fn main() {

    // load config from at_config.json
    let config = Config::load(Path::new("at_config.json")).unwrap();
    let mut at = AtRust::from_config(config);

    at.register_handler(r"^!hello", deneme);
    at.register_handler(r"^.eksi", plugins::eksi::eksi);

    at.connect();

}
