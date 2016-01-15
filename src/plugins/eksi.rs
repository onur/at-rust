

use ::at::{AtRust, AtTrigger};
use plugins::get;


pub fn eksi(trigger: &AtTrigger, at: &AtRust) {
    at.reply(trigger, "EKSI FONKSIYONU CALISTIRILDI");

    let url = format!("https://eksisozluk.com/{}", trigger.command_message);
    let body = get(&url[..]);
}
